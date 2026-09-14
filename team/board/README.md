# The board

Every card is a markdown file in this folder with a front-matter block. The columns are
those `status:` lines rendered — nothing runs, nothing is hosted, and the board versions
with the repository it tracks.

| Field | Values |
|---|---|
| `status` | `need` · `todo` · `doing` · `done` · `held` |
| `owner` | exactly one role slug from `team/roles/` |
| `kind` | `need` (only the human owner can supply it) or `task` (an agent can pick it up) |

A card with two owners is two cards. A card with no owner does not enter the board.
The Conductor owns this folder; see `team/roles/conductor/ROLE.md`.
