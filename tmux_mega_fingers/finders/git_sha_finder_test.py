from ..mark import Mark
from ..targets.sha_target import ShaTarget
from .git_sha_finder import GitShaFinder


def _marks(text: str):
    return GitShaFinder(text, '/tmp').marks


def test_finds_short_sha():
    marks = _marks('commit abc1234 fixes it')
    assert marks == [Mark(start=7, text='abc1234', target=ShaTarget(sha='abc1234'))]


def test_finds_full_sha():
    sha = 'a1b2c3d4e5f6789012345678901234567890abcd'
    marks = _marks(f'git log {sha}')
    assert marks == [Mark(start=8, text=sha, target=ShaTarget(sha=sha))]


def test_ignores_six_hex():
    # 6-char hex (colors) are below the 7-char minimum
    assert _marks('color #ffffff') == []


def test_ignores_diff_blob_shas():
    # `index <hex>..<hex>` blob hashes should not be treated as commit shas
    assert _marks('index c06609e..0f33345 100644') == []


def test_ignores_overlong_hex():
    # >40 hex chars are outside the sha length range
    assert _marks('f' * 45) == []


def test_surrounded_by_hex_matches_whole_token():
    # a hex run of 7..40 chars is one sha, even if it looks like it has a
    # smaller sha embedded (the lookbehind/lookahead keep it as one token)
    tok = 'deadabc1234beef'  # 15 hex chars
    marks = _marks(tok)
    assert marks == [Mark(start=0, text=tok, target=ShaTarget(sha=tok))]
