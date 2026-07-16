import re
from typing import Optional, Pattern, Match

from .finder import BaseFinder
from ..mark import Mark
from ..targets.sha_target import ShaTarget


# Bare hex hashes 7..40 chars. Word-bounded to avoid matching inside longer
# hex tokens. Exclude diff `index <hex>..<hex>` blob hashes via lookbehind on
# `index ` and `.` (the `..` separator). Git short shas (7) and full shas
# (40) still match in `git log` / `jj log` output. False positives on random
# 7+ hex strings are possible but the copy-only action keeps them cheap.
_SHA_RE = re.compile(r'(?<![0-9a-fA-F.])(?<!index )([0-9a-fA-F]{7,40})(?![0-9a-fA-F.])')


class GitShaFinder(BaseFinder):
    """finds git/jujutsu commit hashes"""

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return _SHA_RE

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        start = match.span(1)[0]
        text = match.group(1)

        return Mark(
            start=start,
            text=text,
            target=ShaTarget(sha=text),
        )
