# Upstream origin

Forked from [`artemave/tmux_super_fingers`](https://github.com/artemave/tmux_super_fingers) by Artem Avetisyan.

- Upstream commit: `523dc9b7a79f1ceb8d9be72e22c263c4a7cd3bdf`
- Fork date: 2026-07-14
- New repo: [`megalithic/tmux-mega-fingers`](https://github.com/megalithic/tmux-mega-fingers)

## Fork changes

- Renamed repo, tmux entry script, Python package, config options, and temp error log from `super_fingers`/`super-fingers` to `mega_fingers`/`mega-fingers`.
- Shifted hint letter selects the copy (secondary) action for one selection. Lowercase hint letter selects open (primary) as upstream. Both use the single `@mega-fingers-key` entry. `space` still toggles sticky copy mode.
- Added finders:
  - `git_sha_finder` — git/jujutsu commit hashes (`[0-9a-f]{7,40}`), copy primary.
  - `email_finder` — email addresses, copy primary / OS open secondary.
  - `github_ref_finder` — `owner/repo`, `owner/repo#123`, `#123`, `PR #123`, open in browser primary / copy secondary.
  - `pi_section_finder` — pi-coding-agent output/question boundary markers, disabled by default.
- Implemented mark overlap suppression: earlier finder-order marks win collisions.
- Pane capture uses `capture-pane -J`, so soft-wrapped URLs and paths match as joined logical lines.
- Removed stale `@mega-fingers-secondary-key` binding on source for old local-fork compatibility.
