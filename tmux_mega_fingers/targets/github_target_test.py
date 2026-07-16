from pathlib import Path
import subprocess

from ..actions.copy_to_clipboard_action import CopyToClipboardAction
from ..actions.os_open_action import OsOpenAction
from .github_target import GitHubTarget, remote_origin_url


def test_payload():
    target = GitHubTarget('https://github.com/foo/bar', 'foo/bar')

    assert target.payload.file_or_url == 'https://github.com/foo/bar'
    assert target.payload.url == 'https://github.com/foo/bar'
    assert target.payload.label == 'foo/bar'


def test_primary_action_is_os_open():
    target = GitHubTarget('https://github.com/foo/bar', 'foo/bar')

    assert target.default_primary_action == OsOpenAction


def test_secondary_action_is_copy_to_clipboard():
    target = GitHubTarget('https://github.com/foo/bar', 'foo/bar')

    assert target.default_secondary_action == CopyToClipboardAction


def test_remote_origin_url_supports_https(tmp_path: Path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path)
    subprocess.run(
        ['git', 'remote', 'add', 'origin', 'https://github.com/foo/bar.git'],
        cwd=tmp_path
    )

    assert remote_origin_url(str(tmp_path)) == 'https://github.com/foo/bar'


def test_remote_origin_url_ignores_non_github(tmp_path: Path):
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path)
    subprocess.run(
        ['git', 'remote', 'add', 'origin', 'git@example.com:foo/bar.git'],
        cwd=tmp_path
    )

    assert remote_origin_url(str(tmp_path)) is None
