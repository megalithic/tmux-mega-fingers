from typing import List, Tuple, Type
from ..mark import Mark
from ..utils import flatten
from .rails_log_controller_finder import RailsLogControllerFinder
from .rails_log_partial_finder import RailsLogPartialFinder
from .url_finder import UrlFinder
from .file_path_finder import FilePathFinder
from .diff_file_path_finder import DiffFilePathFinder
from .finder import BaseFinder
# fork additions
from .github_ref_finder import GitHubRefFinder
from .email_finder import EmailFinder
from .git_sha_finder import GitShaFinder
# import image_file_path_finder


class MarkFinder:
    """Finds marks using different finders"""

    # Order matters: path/url/rails finders run first so that real files and
    # full URLs win overlap resolution against the looser fork additions
    # (github slugs, emails, shas), which are ambiguous with path-like text.
    FINDERS: List[Type[BaseFinder]] = [
        RailsLogControllerFinder,
        UrlFinder,
        FilePathFinder,
        RailsLogPartialFinder,
        DiffFilePathFinder,
        GitHubRefFinder,
        EmailFinder,
        GitShaFinder,
        # PiSectionFinder,  # disabled — see pi_section_finder.py docstring
    ]

    def __init__(self, *, finders: List[Type[BaseFinder]] = FINDERS):
        self.finders = finders

    def find_marks(self, text: str, path_prefix: str) -> List[Mark]:
        all_marks = flatten(
            list(map(
                lambda finder_class: finder_class(text, path_prefix).marks,
                self.finders
            ))
        )
        return _remove_overlapping_marks(all_marks)


def _remove_overlapping_marks(marks: List[Mark]) -> List[Mark]:
    """Drop marks that overlap an earlier (finder-order) mark.

    Finders run in FINDERS order, so path/url/rails marks land first and win
    over the looser fork additions (e.g. a github slug that collides with a
    real file path, or a `pull/7` slug inside a github.com URL).
    """
    kept: List[Mark] = []
    spans: List[Tuple[int, int]] = []
    for m in marks:
        s, e = m.start, m.end
        if any(not (e <= ks or s >= ke) for ks, ke in spans):
            continue
        kept.append(m)
        spans.append((s, e))
    return kept
