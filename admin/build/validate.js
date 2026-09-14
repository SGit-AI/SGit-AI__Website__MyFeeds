#!/usr/bin/env node
/* myfeeds.sgit.ai — the release gate.
 *
 *   python3 admin/build/build_pages.py && node admin/build/validate.js
 *
 * Every check here exists because the failure it catches is invisible in the output:
 * a page that renders blank inside a vault frame, a link that 404s for a reader but not
 * for the author, a markdown twin that silently lost half its content, a claim that
 * asserts without a status. Nothing in this file inspects intent — only what shipped.
 *
 * Owned by QA (assertions) and DevOps (the gate). A check that is wrong is a card, not
 * an exception added here.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const failures = [];
const notes = [];
let checks = 0;

function check(ok, message) {
  checks++;
  if (!ok) failures.push(message);
}

function read(p) {
  return fs.readFileSync(path.join(ROOT, p), 'utf8');
}

function exists(p) {
  return fs.existsSync(path.join(ROOT, p));
}

// ---------------------------------------------------------------- the page inventory

const pagesJson = JSON.parse(read('admin/content/pages.json'));
const roleSlugs = fs
  .readdirSync(path.join(ROOT, 'team', 'roles'))
  .filter((d) => fs.existsSync(path.join(ROOT, 'team', 'roles', d, 'ROLE.md')));

const pages = pagesJson.map((p) => p.path).concat(
  ['team/index.html', 'team/board.html', 'team/prompts.html', 'admin/versions.html'],
  roleSlugs.map((s) => `team/roles/${s}.html`)
);

check(pages.length >= 12, `expected the full page set, found ${pages.length}`);

// ------------------------------------------------------------------ per-page checks

const bodies = new Map();

for (const p of pages) {
  if (!exists(p)) {
    failures.push(`${p}: not generated — run build_pages.py`);
    continue;
  }
  const html = read(p);
  bodies.set(p, html);
  const md = p.replace(/\.html$/, '.md');

  // 1. the markdown twin exists and carries content
  check(exists(md), `${p}: markdown twin ${md} is missing`);
  if (exists(md)) {
    const twin = read(md);
    check(twin.length > 400, `${md}: twin is suspiciously short (${twin.length} bytes)`);
    check(
      /^# .+/m.test(twin) && twin.includes('Source: <https://myfeeds.sgit.ai/'),
      `${md}: twin is missing its title or provenance line`
    );
    // The twin must link to markdown, never back into HTML.
    const htmlLinks = [...twin.matchAll(/\]\((?!https?:|mailto:|#)([^)]+)\)/g)]
      .map((m) => m[1])
      .filter((h) => h.endsWith('.html'));
    check(
      htmlLinks.length === 0,
      `${md}: twin links at HTML instead of markdown: ${htmlLinks.slice(0, 3).join(', ')}`
    );
  }

  // 2. THE AUTHORING CONTRACT — a declarative reference to a vault path 404s inside a
  //    sandboxed vault frame, before the bridge installs, and the page renders blank.
  const declarative = [
    ...html.matchAll(/<link\b[^>]*\bhref="([^"]+)"/g),
    ...html.matchAll(/<script\b[^>]*\bsrc="([^"]+)"/g),
    ...html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g),
  ]
    .map((m) => m[1])
    .filter((h) => !/^(https?:|data:|mailto:)/.test(h));
  check(
    declarative.length === 0,
    `${p}: authoring contract violated — declarative vault reference(s): ${declarative.join(', ')}`
  );

  // 3. head furniture: canonical, description, structured data
  check(html.includes(`<link rel="canonical" href="https://myfeeds.sgit.ai/${p}">`),
    `${p}: canonical URL missing or wrong`);
  check(/<meta name="description" content="[^"]{40,}">/.test(html),
    `${p}: description missing or too short to be useful in a search result`);
  const ld = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  check(!!ld, `${p}: no JSON-LD structured data`);
  if (ld) {
    try {
      const parsed = JSON.parse(ld[1]);
      check(parsed['@context'] === 'https://schema.org' && !!parsed.headline,
        `${p}: JSON-LD is present but not well formed`);
    } catch (e) {
      failures.push(`${p}: JSON-LD does not parse — ${e.message}`);
    }
  }

  // 4. readable with JavaScript disabled: the content must be in the served HTML
  const main = html.match(/<main id="main">([\s\S]*?)<\/main>/);
  check(!!main && main[1].replace(/<[^>]+>/g, '').trim().length > 500,
    `${p}: <main> is thin — the page may depend on JavaScript for its content`);
  check(/<h1[^>]*>/.test(html), `${p}: no <h1>`);

  // 5. every inline script parses
  for (const m of html.matchAll(/<script>([\s\S]*?)<\/script>/g)) {
    try {
      new vm.Script(m[1]);
    } catch (e) {
      failures.push(`${p}: inline script does not parse — ${e.message}`);
    }
    checks++;
  }

  // 6. status markers: three permitted values, nothing invented in passing
  const allowed = new Set(['shipped', 'argued', 'unverified', 'need', 'todo', 'doing',
    'done', 'held', 'falsifiable', 'descriptive']);
  for (const m of html.matchAll(/<span class="tag ([a-z]+)"/g)) {
    check(allowed.has(m[1]),
      `${p}: unknown status marker "${m[1]}" — the vocabulary is fixed (see /team/#rules)`);
  }
}

// ------------------------------------------------------------------- link resolution

for (const [p, html] of bodies) {
  const dir = path.posix.dirname(p);
  for (const m of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/g)) {
    const href = m[1];
    if (/^(https?:|mailto:|#)/.test(href)) continue;
    const [target] = href.split('#');
    if (!target) continue;
    const resolved = path.posix.normalize(path.posix.join(dir, target));
    check(exists(resolved), `${p}: broken internal link -> ${href} (${resolved})`);
  }
}

// ------------------------------------------------------------------------- reachable

const reachable = new Set(['index.html']);
let grew = true;
while (grew) {
  grew = false;
  for (const from of [...reachable]) {
    const html = bodies.get(from);
    if (!html) continue;
    const dir = path.posix.dirname(from);
    for (const m of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/g)) {
      if (/^(https?:|mailto:|#)/.test(m[1])) continue;
      const t = path.posix.normalize(path.posix.join(dir, m[1].split('#')[0]));
      if (bodies.has(t) && !reachable.has(t)) {
        reachable.add(t);
        grew = true;
      }
    }
  }
}
for (const p of pages) {
  check(reachable.has(p), `${p}: orphan — not reachable by following links from index.html`);
}

// ----------------------------------------------------------------- site-wide outputs

for (const f of ['llms.txt', 'llms-full.txt', 'sitemap.xml', 'robots.txt', 'CNAME',
  'app.json', 'data/team.json', 'assets/site.css', 'assets/site.js']) {
  check(exists(f), `${f}: missing`);
}

if (exists('llms.txt')) {
  const llms = read('llms.txt');
  for (const p of pages) {
    check(llms.includes(`/${p.replace(/\.html$/, '.md')}`),
      `llms.txt: does not index ${p} — an agent starting there cannot reach it`);
  }
}

if (exists('llms-full.txt')) {
  const full = read('llms-full.txt');
  for (const p of pages) {
    check(full.includes(`# /${p}`), `llms-full.txt: missing the section for ${p}`);
  }
}

if (exists('CNAME')) {
  check(read('CNAME').trim() === 'myfeeds.sgit.ai', 'CNAME: not myfeeds.sgit.ai');
}

// ------------------------------------------------------- the roster matches the disk

if (exists('data/team.json')) {
  const team = JSON.parse(read('data/team.json'));
  check(team.roles.length === roleSlugs.length,
    `data/team.json: ${team.roles.length} roles served, ${roleSlugs.length} ROLE.md files on disk`);
  check(team.totals.roles === team.roles.length,
    'data/team.json: the roles count does not match the roles it serves');
  for (const r of team.roles) {
    check(roleSlugs.includes(r.slug), `data/team.json: role "${r.slug}" has no ROLE.md`);
    check(!!r.not_responsible_for && r.not_responsible_for.length > 20,
      `${r.slug}: a role without an exclusion list is not a role`);
    check(r.claim_form === 'falsifiable',
      `${r.slug}: Central Claim is "${r.claim_form}" — this site writes claims as failure conditions`);
  }
  // Every open card names a real role.
  for (const c of team.board) {
    check(roleSlugs.includes(c.owner), `board card ${c.id}: owner "${c.owner}" is not a role`);
  }
}

// --------------------------------------------------------------- assets parse-checked

if (exists('assets/site.js')) {
  try {
    new vm.Script(read('assets/site.js'));
  } catch (e) {
    failures.push(`assets/site.js: does not parse — ${e.message}`);
  }
  checks++;
}
if (exists('assets/site.css')) {
  const css = read('assets/site.css');
  const opens = (css.match(/{/g) || []).length;
  const closes = (css.match(/}/g) || []).length;
  check(opens === closes, `assets/site.css: ${opens} { against ${closes} } — unbalanced`);
}

// ------------------------------------------------------------------- banned patterns

for (const [p, html] of bodies) {
  // Case-sensitive on purpose: "todo" is a legitimate board status and appears in
  // class names and fragment links. A placeholder left in prose is shouted.
  const prose = html.replace(/<[^>]+>/g, ' ');
  check(!/\bTODO\b|\bFIXME\b|\bXXX\b/.test(prose) && !/lorem ipsum/i.test(prose),
    `${p}: carries a placeholder (TODO / FIXME / XXX / lorem ipsum)`);
  check(!/<span class="tag">\s*<\/span>/.test(html), `${p}: empty status marker`);
}

// -------------------------------------------------------------------------- report

if (notes.length) notes.forEach((n) => console.log(`note: ${n}`));

if (failures.length) {
  console.error(`\nvalidate: ${failures.length} failure(s) across ${checks} checks\n`);
  failures.forEach((f) => console.error(`  ✗ ${f}`));
  console.error('');
  process.exit(1);
}

console.log(`validate: ${checks} checks passed across ${pages.length} pages ` +
  `(${roleSlugs.length} roles, ${reachable.size} reachable from the front page)`);
