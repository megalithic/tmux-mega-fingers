"""pi-coding-agent output section finder  (DISABLED by default)

Intent: highlight boundaries between pi's agent output, user questions, and
input entries so you can quickly copy a whole section from a pi pane.

STATUS: not registered in MarkFinder.FINDERS. The exact on-screen markers pi
uses for agent/user/entry boundaries are not yet confirmed, so shipping a
guessed pattern would create noisy false-positive marks. Once the markers are
known, tune ``PI_SECTION_PATTERNS`` below and add ``PiSectionFinder`` to
``finders/__init__.py``'s ``FINDERS`` list.

Candidate markers to confirm against a live pi pane (run `tmux capture-pane`):
  - user input line:        leading prompt glyph, e.g. ``❯ `` or ``> ``
  - assistant output start: a blank line or a leading bullet
  - tool/entry boundary:    ``●`` / ``→`` / dashed rule

Each match produces a CopyToClipboardAction mark on the marker text itself; to
copy a *section* (not just the marker) you'd extend this to compute the span
from one marker to the next — that needs multi-line span support, which the
current finder API (single-line, ``start``/``text``) does not provide. File as
a follow-up if you want true section selection.
"""

import re
from typing import Optional, Pattern, List

from .finder import BaseFinder
from ..mark import Mark
from ..targets.target import Target
from ..targets.target_payload import OsOpenable
from ..actions.action import Action
from ..actions.copy_to_clipboard_action import CopyToClipboardAction


class _PiSectionPayload(OsOpenable):
    def __init__(self, text: str):
        self._text = text

    @property
    def file_or_url(self) -> str:
        return self._text


class _PiSectionTarget(Target):
    primary_action = CopyToClipboardAction
    secondary_action = CopyToClipboardAction

    def __init__(self, text: str):
        self._text = text

    @property
    def payload(self) -> _PiSectionPayload:
        return _PiSectionPayload(self._text)

    @property
    def default_primary_action(self) -> type:
        return CopyToClipboardAction

    @property
    def default_secondary_action(self) -> type:
        return CopyToClipboardAction


# Tune these once markers are confirmed. Empty list => finder yields no marks.
PI_SECTION_PATTERNS: List[Pattern[str]] = [
    # re.compile(r'^(❯|›|>)\s'),           # user input prompt glyph
    # re.compile(r'^(●|→|—{3,})\s?'),      # tool / section rule
]


class PiSectionFinder(BaseFinder):
    """finds pi-coding-agent section boundaries (stub — see module docstring)"""

    @classmethod
    def pattern(cls) -> Pattern[str]:
        if not PI_SECTION_PATTERNS:
            # never matches
            return re.compile(r'(?!x)x')
        return re.compile('|'.join(p.pattern for p in PI_SECTION_PATTERNS))

    def match_to_mark(self, match) -> Optional[Mark]:
        text = match.group(0)
        return Mark(
            start=match.span()[0],
            text=text,
            target=_PiSectionTarget(text),
        )
