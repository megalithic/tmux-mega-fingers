import re
import subprocess
from dataclasses import dataclass
from typing import Type, Optional
from .target import Target
from .target_payload import OsOpenable
from ..actions.action import Action
from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from ..actions.os_open_action import OsOpenAction


def remote_origin_url(cwd: str) -> Optional[str]:
    """Return the HTTPS github URL for the current repo's origin, or None.

    Used to resolve bare `#123` / `PR #123` refs against the repo you're in.
    """
    try:
        out = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            cwd=cwd, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return None
    return _normalize_git_url(out)


def _normalize_git_url(url: str) -> Optional[str]:
    # git@github.com:owner/repo.git  -> https://github.com/owner/repo
    m = re.match(r'(?:git@|https://)github\.com[:/](.+?)(?:\.git)?$', url)
    if not m:
        return None
    return f'https://github.com/{m.group(1)}'


class GitHubPayload(OsOpenable):
    def __init__(self, url: str, label: str):
        self._url = url
        self._label = label

    @property
    def file_or_url(self) -> str:
        return self._url

    @property
    def url(self) -> str:
        return self._url

    @property
    def label(self) -> str:
        return self._label


@dataclass
class GitHubTarget(Target):
    url: str
    label: str

    @property
    def payload(self) -> GitHubPayload:
        return GitHubPayload(self.url, self.label)

    @property
    def default_primary_action(self) -> Type[Action]:
        return OsOpenAction

    @property
    def default_secondary_action(self) -> Type[Action]:
        return CopyToClipboardAction
