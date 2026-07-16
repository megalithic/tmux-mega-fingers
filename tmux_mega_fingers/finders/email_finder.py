import re
from typing import Optional, Pattern, Match

from .finder import BaseFinder
from ..mark import Mark
from ..targets.email_target import EmailTarget


# RFC-ish local-part@domain.tld. Keep it pragmatic: local part is alnum/._%+-,
# domain is alnum.- with at least one dot and a 2+ char TLD.
_EMAIL_RE = re.compile(
    r'(?<![A-Za-z0-9._%+-])'
    r'([A-Za-z0-9._%+-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?'
    r'(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+)'
)


class EmailFinder(BaseFinder):
    """finds email addresses"""

    @classmethod
    def pattern(cls) -> Pattern[str]:
        return _EMAIL_RE

    def match_to_mark(self, match: Match[str]) -> Optional[Mark]:
        start = match.span(1)[0]
        text = match.group(1)

        return Mark(
            start=start,
            text=text,
            target=EmailTarget(email=text),
        )
