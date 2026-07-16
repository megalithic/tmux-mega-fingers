from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from ..actions.os_open_action import OsOpenAction
from .email_target import EmailTarget


def test_payload():
    target = EmailTarget('seth@example.com')

    assert target.payload.file_or_url == 'mailto:seth@example.com'
    assert target.payload.email == 'seth@example.com'


def test_primary_action_is_copy_to_clipboard():
    target = EmailTarget('seth@example.com')

    assert target.default_primary_action == CopyToClipboardAction


def test_secondary_action_is_os_open():
    target = EmailTarget('seth@example.com')

    assert target.default_secondary_action == OsOpenAction
