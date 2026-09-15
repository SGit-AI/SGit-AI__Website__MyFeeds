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

const roleSlugs = fs
  .readdirSync(path.join(ROOT, 'team', 'roles'))
  .filter((d) => fs.existsSync(path.join(ROOT, 'team', 'roles', d, 'ROLE.md')));

// The build publishes what it made. This file used to re-derive the list — pages.json
// plus a hardcoded set of generated paths — and when the back office shipped it went on
// checking 19 pages out of 38 and reporting success. A checker that maintains its own
// idea of what exists will eventually check something else.
if (!exists('data/site.json')) {
  failures.push('data/site.json: missing — run the build; the validator reads its inventory');
}
const inventory = exists('data/site.json') ? JSON.parse(read('data/site.json')) : { pages: [] };
const pages = inventory.pages.map((p) => p.path);

check(pages.length >= 12, `expected the full page set, found ${pages.length}`);
check(inventory.counts && inventory.counts.pages === pages.length,
  'data/site.json: the page count disagrees with the pages it lists');
// Everything registered in pages.json must be in the inventory: a page dropped from the
// build would otherwise simply stop being checked.
for (const p of JSON.parse(read('admin/content/pages.json'))) {
  check(pages.includes(p.path), `${p.path}: registered in pages.json but not built`);
}
for (const slug of roleSlugs) {
  check(pages.includes(`team/roles/${slug}.html`), `${slug}: has a ROLE.md but no page`);
}

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
    'done', 'held', 'falsifiable', 'descriptive', 'open', 'answered']);
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

// ------------------------------------------------ version, versions/ and the deploy gate

// The version is owned by one file, and the workflow every *.sgit.ai site shares reads
// it. If the pages, the log and that file disagree, a release tags one version and
// publishes another.
const VERSION = read('admin/build/version.txt').trim();
check(/^v\d+\.\d+\.\d+$/.test(VERSION),
  `admin/build/version.txt: "${VERSION}" is not vMAJOR.MINOR.PATCH`);

if (exists('versions/index.json')) {
  const idx = JSON.parse(read('versions/index.json'));
  check(idx.current === VERSION,
    `versions/index.json: current is ${idx.current}, version.txt says ${VERSION}`);
  check(idx.versions.length > 0 && idx.versions[0].version === VERSION,
    'versions/index.json: the newest entry is not the current version');
  for (const v of idx.versions) {
    const f = `versions/${v.version}.json`;
    check(exists(f), `${f}: indexed but missing`);
    if (!exists(f)) continue;
    const entry = JSON.parse(read(f));
    check(entry.version === v.version, `${f}: version field disagrees with the index`);
    check(/^\d{4}-\d{2}-\d{2}$/.test(entry.date), `${f}: date is not YYYY-MM-DD`);
    // "title is a sentence, not a label" — the estate's own guidance. A label is short
    // and says nothing; there is no way to check prose, but there is a way to catch
    // "UI improvements".
    check(typeof entry.title === 'string' && entry.title.length >= 25,
      `${f}: title "${entry.title}" reads as a label — it should be a sentence saying what changed`);
    check(Array.isArray(entry.changes) && entry.changes.length > 0,
      `${f}: no changes listed`);
    check(!!entry.commit_ref, `${f}: no commit reference — a version that does not name what it was built from cannot be verified later`);
  }
}

// The version badge must be a LINK, to THAT version's own entry.
for (const [p, html] of bodies) {
  const m = html.match(/<a class="ver" href="([^"]+)"/);
  check(!!m, `${p}: the version badge is not a link — a reader who clicks ${VERSION} wants to know what ${VERSION} was`);
  if (m) {
    const [target, frag] = m[1].split('#');
    const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(p), target));
    check(exists(resolved), `${p}: version badge points at a missing page (${resolved})`);
    check(frag === VERSION.replace(/\./g, '-'),
      `${p}: version badge links to #${frag}, expected the anchor for ${VERSION}`);
    if (exists(resolved)) {
      check(read(resolved).includes(`id="${frag}"`),
        `admin/versions.html: no entry with id="${frag}" for the badge to land on`);
    }
  }
  check(html.includes(`>${VERSION}<`), `${p}: does not show ${VERSION}`);
}

// "Anything rendered stays one click from its bytes."
for (const [p, html] of bodies) {
  const twin = p.replace(/\.html$/, '.md');
  const dir = path.posix.dirname(p);
  // Resolve every link on the page rather than matching one spelling: "index.md" and
  // "../thesis/index.md" are both correct from thesis/index.html, and a check that
  // accepts only one of them tests the generator's style, not the site's property.
  const linksToTwin = [...html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/g)]
    .map((m) => m[1])
    .filter((h) => !/^(https?:|mailto:|#)/.test(h))
    .some((h) => path.posix.normalize(path.posix.join(dir, h.split('#')[0])) === twin);
  check(linksToTwin,
    `${p}: does not link its own markdown twin (${twin}) — a page that only shows its own interpretation asks to be trusted`);
}

// Deny by default in app.json, with the reason for any grant written down.
if (exists('app.json')) {
  const app = JSON.parse(read('app.json'));
  check(app.version === VERSION, `app.json: version is ${app.version}, expected ${VERSION}`);
  check(Object.prototype.hasOwnProperty.call(app, 'permissions'),
    'app.json: no permissions key — declare the narrowest set that works, even if that is {}');
  check(!!app.permissions_note,
    'app.json: permissions carry no note saying why each grant exists');
}

// The canonical host and CNAME have to agree, or the site publishes canonical URLs
// pointing at a domain it is not served from.
if (exists('CNAME')) {
  const host = read('CNAME').trim();
  for (const [p, html] of bodies) {
    check(html.includes(`<link rel="canonical" href="https://${host}/`),
      `${p}: canonical host disagrees with CNAME (${host})`);
  }
}

// The deploy pipeline itself: it is the estate's, and the release contract depends on
// the three jobs existing in order.
if (exists('.github/workflows/deploy-pages.yml')) {
  const wf = read('.github/workflows/deploy-pages.yml');
  for (const job of ['validate:', 'tag-release:', 'deploy:']) {
    check(wf.includes(`  ${job}`), `deploy-pages.yml: no ${job.slice(0, -1)} job`);
  }
  check(wf.includes('actions/deploy-pages@v4'), 'deploy-pages.yml: does not deploy');
  check(wf.includes("--exclude '.sg_vault'"),
    'deploy-pages.yml: the artifact does not exclude .sg_vault');
  check(/needs:\s*\[validate, tag-release\]/.test(wf),
    'deploy-pages.yml: deploy is not gated on validate');
  // The workflow reads version.txt; if the generator stopped owning it there, a release
  // would tag one version and publish another.
  check(wf.includes('admin/build/version.txt'),
    'deploy-pages.yml: does not read admin/build/version.txt');
  check(read('admin/build/build_pages.py').includes('VERSION_FILE'),
    'build_pages.py: no longer reads version.txt, which the deploy workflow depends on');
} else {
  failures.push('.github/workflows/deploy-pages.yml: missing — nothing publishes this site');
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

// ------------------------------------------------------- recovered content actually renders

// Markdown image syntax rendered as literal text on every recovered architecture post for
// two releases, because the inline-markdown link rule required non-empty link text and
// `![](url)` has none — so it matched nothing and fell through as source. Nothing failed;
// it just looked wrong to a human and to nobody else.
for (const [p, html] of bodies) {
  // Scope to <main>: a description built from a post body legitimately mentions markdown
  // before it is cleaned, and head metadata is not rendered content.
  // Scope to <main>, then drop code spans and blocks. Markdown syntax inside <code> is
  // the correct rendering of a page that documents markdown — this check failed the build
  // on a board card whose whole subject was that `![](url)` had never been handled.
  const mainOnly = (html.match(/<main id="main">([\s\S]*?)<\/main>/) || ['', ''])[1]
    .replace(/<pre[\s\S]*?<\/pre>/g, '')
    .replace(/<code>[\s\S]*?<\/code>/g, '');
  const raw = [...mainOnly.matchAll(/!\[[^\]]*\]\([^)]*\)/g)];
  check(raw.length === 0,
    `${p}: ${raw.length} markdown image(s) rendered as literal source, not as <img>`);
  const rawLinks = [...mainOnly.matchAll(/(^|[^!])\[[^\]]+\]\(https?:[^)]*\)/g)];
  check(rawLinks.length === 0,
    `${p}: ${rawLinks.length} markdown link(s) rendered as literal source`);
}

// Every image a recovered post points at is either in this repository or is explicitly
// marked as not recovered. A broken <img> is the one outcome that is not allowed, because
// it looks identical to an image that simply failed to load this once.
{
  const archiveRoot = 'back-office/archive/mvp.myfeeds.ai';
  let local = 0, missing = 0, offsite = 0;
  for (const [p, html] of bodies) {
    for (const m of [...html.matchAll(/<img[^>]*\bsrc="([^"]+)"/g),
                     ...html.matchAll(/<a class="rimg" href="([^"]+)"/g)]) {
      const src = m[1];
      if (/^(https?:|data:)/.test(src)) {
        failures.push(`${p}: recovered image still points off-site (${src})`);
        continue;
      }
      const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(p), src));
      check(exists(resolved), `${p}: <img> points at a file that is not here (${resolved})`);
      if (resolved.startsWith(archiveRoot)) local++;
    }
    missing += (html.match(/class="missing-img"/g) || []).length;
    offsite += (html.match(/class="offsite-img"/g) || []).length;
  }
  if (local || missing || offsite) {
    notes.push(`recovered images: ${local} served from this repository, ${missing} never `
      + `archived (re-running the archiver will not find them), ${offsite} embedded from `
      + `other hosts and never part of this site`);
  }
}

// --------------------------------------------------------------- AI provenance is stated

// The site is written by a model. Saying so once, somewhere, is not disclosure: a reader
// arrives on a deep page from a search result and never sees the homepage. Every page
// carries its own review status, and every page links the page that explains it.
for (const [p, html] of bodies) {
  check(/<p class="prov">/.test(html),
    `${p}: no review status — every page states whether a human has read it`);
  check(/generated by an AI system/.test(html),
    `${p}: no AI-generation disclosure in the footer`);
}

// ------------------------------------------------- nothing non-deterministic is tracked

// CI rebuilds on a clean checkout and fails if the tree differs by a byte. Any tracked
// file the build REWRITES with different bytes each run therefore breaks every push,
// whatever the change was. A .pyc did exactly that: the .gitignore negation that
// un-ignores admin/build/ (so the generator is tracked at all) also un-ignored
// __pycache__, and Python rewrites those on every import.
{
  const tracked = require('child_process')
    .execSync('git ls-files', { cwd: ROOT, encoding: 'utf8' })
    .split('\n').filter(Boolean);
  const junk = tracked.filter((f) =>
    /(^|\/)__pycache__\//.test(f) || /\.py[cod]$/.test(f) ||
    /(^|\/)\.DS_Store$/.test(f) || /(^|\/)node_modules\//.test(f));
  check(junk.length === 0,
    `tracked build artefact(s) will break the staleness check on every push: ${junk.join(', ')}`);
  // The generator and the gate must BE tracked — the .gitignore that hides bytecode is
  // one edit away from hiding them too.
  for (const need of ['admin/build/build_pages.py', 'admin/build/validate.js',
    'admin/build/backoffice.py', 'admin/build/version.txt']) {
    check(tracked.includes(need), `${need}: not tracked by git — check .gitignore`);
  }
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
