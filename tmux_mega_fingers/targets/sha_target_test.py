from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from .sha_target import ShaTarget


def test_payload():
    target = ShaTarget('1234567')

    assert target.payload.file_or_url == '1234567'
    assert target.payload.sha == '1234567'


def test_primary_action_is_copy_to_clipboard():
    target = ShaTarget('1234567')

    assert target.default_primary_action == CopyToClipboardAction


def test_secondary_action_is_copy_to_clipboard():
    target = ShaTarget('1234567')

    assert target.default_secondary_action == CopyToClipboardAction
