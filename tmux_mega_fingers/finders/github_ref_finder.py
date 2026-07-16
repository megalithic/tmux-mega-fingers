import os
import re
from typing import Optional, Pattern, Match

from .finder import BaseFinder
from ..mark import Mark
from ..targets.github_target import GitHubTarget, remote_origin_url


# owner segment (github user/org): alphanumeric + hyphens, no dot/underscore.
# repo segment: differs between the #issue form and the bare slug form (below).
_OWNER = r'[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?'

# slug_issue: owner/repo#123 — the trailing #num is a strong github signal, so
# the repo segment may contain dots (e.g. owner/repo.io#42).
_REPO_WITH_DOTS = r'[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?'

# bare slug: owner/repo with no #num — ambiguous with file paths, so require
# the owner to be at least 2 chars (drops diff `a/x`/`b/x` noise; single-char
# github owners are vanishingly rare) and the repo segment to have NO dot
# (drops `controllers/orders_controller.rb`-style filename paths while keeping
# plain `owner/repo`).
_OWNER_MIN2 = r'[A-Za-z0-9]{2,}(?:[A-Za-z0-9-]*[A-Za-z0-9])?'
_REPO_NO_DOTS = r'[A-Za-z0-9](?:[A-Za-z0-9_-]*[A-Za-z0-9])?'


class GitHubRefFinder(BaseFinder):
    """finds github repo/issue/PR references

    Matches:
      - owner/repo#123   -> https://github.com/owner/repo/issues/123
      - owner/repo        -> https://github.com/owner/repo  (repo segment has no
                              dot, to avoid matching filename-like paths)
      - #123 / PR #123    -> <current repo>/issues/123 (needs an origin remote)

    github.com URLs are already caught by UrlFinder, so only slug/short forms
    are handled here. A leading lookbehind on each alternative (and `/` in it)
    stops URL path segments (e.g. `pull/7`) matching.
    """

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return re.compile(
            r'(?P<slug_issue>(?<![A-Za-z0-9._@/-])' + _OWNER + r'/' + _REPO_WITH_DOTS + r'#\d+)'
            r'|(?P<slug>(?<![A-Za-z0-9._@/-])' + _OWNER_MIN2 + r'/' + _REPO_NO_DOTS + r')(?![A-Za-z0-9#/.-])'
            r'|(?P<bare>(?<![A-Za-z0-9_#])#\d+)(?![A-Za-z0-9_])'
        )

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        text = match.group(0)
        start = match.span()[0]

        if match.group('slug_issue'):
            slug, num = text.rsplit('#', 1)
            url = f'https://github.com/{slug}/issues/{num}'
            return Mark(start=start, text=text, target=GitHubTarget(url=url, label=text))

        if match.group('slug'):
            slug = text
            # defer to FilePathFinder if it's a real local path
            candidate = os.path.join(self.path_prefix, slug)
            if os.path.exists(candidate):
                return None
            url = f'https://github.com/{slug}'
            return Mark(start=start, text=text, target=GitHubTarget(url=url, label=text))

        if match.group('bare'):
            num = text[1:]
            repo = remote_origin_url(self.path_prefix)
            if not repo:
                return None
            url = f'{repo}/issues/{num}'
            return Mark(start=start, text=text, target=GitHubTarget(url=url, label=text))

        return None
