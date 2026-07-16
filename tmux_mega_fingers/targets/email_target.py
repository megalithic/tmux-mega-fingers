from dataclasses import dataclass
from typing import Type
from .target import Target
from .target_payload import OsOpenable
from ..actions.action import Action
from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from ..actions.os_open_action import OsOpenAction


class EmailPayload(OsOpenable):
    def __init__(self, email: str):
        self._email = email

    @property
    def file_or_url(self) -> str:
        # OS open of a mailto: launches the default mail client
        return f'mailto:{self._email}'

    @property
    def email(self) -> str:
        return self._email


@dataclass
class EmailTarget(Target):
    email: str

    @property
    def payload(self) -> EmailPayload:
        return EmailPayload(self.email)

    @property
    def default_primary_action(self) -> Type[Action]:
        return CopyToClipboardAction

    @property
    def default_secondary_action(self) -> Type[Action]:
        return OsOpenAction
