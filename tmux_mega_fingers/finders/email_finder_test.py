from ..mark import Mark
from ..targets.email_target import EmailTarget
from .email_finder import EmailFinder


def _marks(text: str):
    return EmailFinder(text, '/tmp').marks


def test_finds_simple_email():
    marks = _marks('mail me at seth@example.com please')
    assert marks == [
        Mark(start=11, text='seth@example.com', target=EmailTarget(email='seth@example.com'))
    ]


def test_finds_subdomain_email():
    marks = _marks('dev@sub.example.co.uk here')
    assert marks == [
        Mark(
            start=0,
            text='dev@sub.example.co.uk',
            target=EmailTarget(email='dev@sub.example.co.uk')
        )
    ]


def test_secondary_payload_is_mailto():
    marks = _marks('a@b.co')
    assert marks[0].target.payload.file_or_url == 'mailto:a@b.co'


def test_ignores_bare_at():
    assert _marks('not an @ handle') == []
