import os
import subprocess

import pytest

from ..mark import Mark
from ..targets.github_target import GitHubTarget, _remote_origin_url
from .github_ref_finder import GitHubRefFinder


def _marks(text: str, path_prefix: str = '/tmp'):
    return GitHubRefFinder(text, path_prefix).marks


def test_slug_issue():
    marks = _marks('see owner/repo#99')
    assert marks == [Mark(start=4, text='owner/repo#99', target=GitHubTarget(url='https://github.com/owner/repo/issues/99', label='owner/repo#99'))]


def test_bare_slug():
    marks = _marks('open foo/bar in browser')
    assert marks == [Mark(start=5, text='foo/bar', target=GitHubTarget(url='https://github.com/foo/bar', label='foo/bar'))]


def test_slug_with_dots_rejected_for_bare():
    # repo segment that ends in `.ext` (no dotless prefix to backtrack to)
    # is not matched as a slug
    assert _marks('see foo/bar.txt') == []


def test_slug_prefix_of_path_still_matches_if_no_dot():
    # `controllers/orders` (no dot) genuinely looks like a slug, so it matches;
    # the trailing `_controller.rb` is left unmatched. This is inherent
    # ambiguity, accepted for the bare-slug case.
    marks = _marks('see controllers/orders_controller.rb')
    assert marks == [Mark(start=4, text='controllers/orders', target=GitHubTarget(url='https://github.com/controllers/orders', label='controllers/orders'))]


def test_slug_issue_allows_dots():
    marks = _marks('owner/repo.io#42')
    assert marks == [Mark(start=0, text='owner/repo.io#42', target=GitHubTarget(url='https://github.com/owner/repo.io/issues/42', label='owner/repo.io#42'))]


def test_url_path_segment_not_matched():
    # `pull/7` inside a github.com URL must not be matched as a slug
    assert _marks('https://github.com/foo/bar/pull/7') == []


def test_diff_a_b_not_matched():
    # single-char owners (diff `a/x` `b/x`) should not match
    assert _marks('diff --git a/x b/x') == []


def test_bare_issue_without_remote(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path)
    assert _marks('fix #42', str(tmp_path)) == []


def test_bare_issue_with_remote(tmp_path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path)
    subprocess.run(['git', 'remote', 'add', 'origin', 'git@github.com:foo/bar.git'], cwd=tmp_path)
    marks = _marks('fix #42', str(tmp_path))
    assert marks == [Mark(start=4, text='#42', target=GitHubTarget(url='https://github.com/foo/bar/issues/42', label='#42'))]


def test_hex_color_hash_not_matched():
    # `#123abc` is not a bare issue (trailing letters block the digit-only match)
    assert _marks('color #123abc') == []


def test_slug_defers_to_existing_file(tmp_path):
    os.makedirs(os.path.join(tmp_path, 'foo'))
    # foo/bar does not exist under tmp_path, so it still matches as a slug
    assert _marks('foo/bar', str(tmp_path)) != []
    # foo (dir) exists but foo/bar does not -> still a slug (no defer)
    # create foo/bar as a file to confirm defer
    open(os.path.join(tmp_path, 'foo', 'bar'), 'w').close()
    assert _marks('foo/bar', str(tmp_path)) == []
