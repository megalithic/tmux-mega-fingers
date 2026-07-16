from dataclasses import dataclass
from typing import Type
from .target import Target
from .target_payload import OsOpenable
from ..actions.action import Action
from ..actions.copy_to_clipboard_action import CopyToClipboardAction


class ShaPayload(OsOpenable):
    """A git/jujutsu commit hash."""

    def __init__(self, sha: str):
        self._sha = sha

    @property
    def file_or_url(self) -> str:
        return self.sha

    @property
    def sha(self) -> str:
        return self._sha


@dataclass
class ShaTarget(Target):
    sha: str

    @property
    def payload(self) -> ShaPayload:
        return ShaPayload(self.sha)

    @property
    def default_primary_action(self) -> Type[Action]:
        # most useful: copy the sha to clipboard
        return CopyToClipboardAction

    @property
    def default_secondary_action(self) -> Type[Action]:
        # bare sha has no open target without repo context; copy again
        return CopyToClipboardAction
