# Tmux Mega Fingers

A tmux mode that marks file paths, URLs, emails, GitHub refs, and git hashes across panes, then opens or copies the selected target.

This fork is based on [`artemave/tmux_super_fingers`](https://github.com/artemave/tmux_super_fingers) by Artem Avetisyan. Original project ideas, architecture, and most code come from that repo. See [UPSTREAM.md](./UPSTREAM.md) for the upstream commit and fork notes.

<p align="center">
<img width="300" src="https://78.media.tumblr.com/e1712952f6eb24f418a997a8da6ae831/tumblr_ou1znif6LW1w4t58uo1_500.gif" />
</p>

## What changed from upstream

- Shifted hint letter selects the secondary copy action for one selection. Lowercase keeps the primary open action. `space` still toggles sticky secondary mode.
- Finder overlap suppression keeps earlier finder-order marks when patterns collide.
- Added finders:
  - `git_sha_finder` — git/jujutsu hashes, copy primary.
  - `email_finder` — email addresses, copy primary / `mailto:` open secondary.
  - `github_ref_finder` — `owner/repo`, `owner/repo#123`, bare `#123`, and `PR #123`.
  - `pi_section_finder` — disabled until marker patterns are tuned.
- Pane capture uses `capture-pane -J`, so soft-wrapped URLs and paths match as joined logical lines.

## Install

Requires Python >= 3.9.

### TPM

```tmux
set -ga update-environment EDITOR
set -g @plugin 'megalithic/tmux-mega-fingers'
set -g @mega-fingers-key 'C-f'
```

Then press <kbd>prefix</kbd> + <kbd>I</kbd> to install TPM plugins.

### Manual

```bash
git clone https://github.com/megalithic/tmux-mega-fingers.git ~/.tmux/plugins/tmux-mega-fingers
```

```tmux
set -ga update-environment EDITOR
run-shell ~/.tmux/plugins/tmux-mega-fingers/tmux_mega_fingers.tmux
```

Reload tmux config:

```bash
tmux source-file ~/.tmux.conf
```

## Usage

Enter fingers mode with <kbd>prefix</kbd> + configured key. Default key: <kbd>f</kbd>.

- Press lowercase hint: primary action, usually open.
- Press shifted hint: secondary action, usually copy.
- Press <kbd>space</kbd>: toggle sticky secondary mode.

## Configuration

### `@mega-fingers-key`

Customize fingers mode entry key. Always preceded by tmux prefix.

```tmux
set -g @mega-fingers-key 'C-f'
```

### `@mega-fingers-extend`

Load a Python extension file that changes target actions.

```tmux
set -g @mega-fingers-extend /path/to/actions.py
```

Example:

```python3
import os
from .targets.file_target import FileTarget
from .actions.send_to_vim_in_tmux_pane_action import SendToVimInTmuxPaneAction
from .actions.action import Action
from .targets.target_payload import EditorOpenable


class SendToVsCodeAction(Action):
    def __init__(self, target_payload: EditorOpenable):
        self.target_payload = target_payload

    def perform(self):
        path = self.target_payload.file_path

        if self.target_payload.line_number:
            path += f':{self.target_payload.line_number}'

        os.system(f'code -g {path}')


FileTarget.primary_action = SendToVsCodeAction
FileTarget.secondary_action = SendToVimInTmuxPaneAction
```

See existing actions in [`tmux_mega_fingers/actions`](./tmux_mega_fingers/actions).

## Troubleshooting

Check the error log:

```bash
tail -F /tmp/tmux_mega_fingers_error.txt
```

If text files open in another editor, ensure `EDITOR` is exactly `vim` or `nvim`.

## Development

```bash
git clone https://github.com/megalithic/tmux-mega-fingers.git
cd tmux-mega-fingers
pipenv install --dev
npm install
make
```

## License

MIT. See [LICENSE](./LICENSE). Original license from `artemave/tmux_super_fingers` is preserved.
