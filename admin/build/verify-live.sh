#!/usr/bin/env bash
# The last step of a release, and the only one that can tell you the truth.
#
# "Both remotes in sync" is NOT the same as "live". On the main site that gap cost two
# releases in one afternoon: v0.2.31 and v0.2.32 both pushed cleanly and both reported
# success, while GitHub Pages failed to deploy either — codeload returned 429 for
# actions/configure-pages and the deploy job died before running a step. The site served
# a two-release-old page for forty minutes and nothing noticed, because the failure was
# in a job neither remote knows about.
#
# So the last thing a release does is ask the live site what version it is serving.
#
#   ./admin/build/verify-live.sh            # waits for version.txt's version
#   ./admin/build/verify-live.sh v0.1.4     # waits for a specific one
#
# Exits non-zero if the site never serves it. Do not report a release as live without
# this having passed.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
host="$(tr -d '[:space:]' < "$here/../../CNAME")"
want="${1:-$(tr -d '[:space:]' < "$here/version.txt")}"

[ -n "$host" ] || { echo "verify-live: CNAME is empty" >&2; exit 2; }
[ -n "$want" ] || { echo "verify-live: no version to wait for" >&2; exit 2; }

echo "verify-live: waiting for $want at https://$host/ (up to 8 min)"
live=""
for i in $(seq 1 32); do
  sleep 15
  # Cache-buster: GitHub Pages serves max-age=600 and we want the origin's answer.
  live="$(curl -sS --max-time 20 "https://$host/index.html?deploycheck=$i" 2>/dev/null \
          | grep -o 'v[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1 || true)"
  [ "$live" = "$want" ] && break
  printf '.'
done
echo

if [ "$live" = "$want" ]; then
  echo "verify-live: $host is serving $want"
  exit 0
fi

cat >&2 <<MSG
verify-live: $host is serving ${live:-<nothing readable>}, expected $want
  The push succeeded — this is the GitHub Pages deploy, not the content.
  Check:  https://github.com/SGit-AI/SGit-AI__Website__MyFeeds/actions
  A 429 downloading actions/configure-pages is transient; re-run the job.
  If the host does not resolve at all, this site is not deployed yet — board card 004.
pushed but NOT published — do not report this release as live
MSG
exit 1
