from ..mark import Mark
from ..targets.url_target import UrlTarget
from . import remove_overlapping_marks


def test_remove_overlapping_marks_keeps_earlier_mark():
    marks = [
        Mark(start=0, text='https://github.com/foo/bar', target=UrlTarget('https://github.com/foo/bar')),
        Mark(start=19, text='foo/bar', target=UrlTarget('https://github.com/foo/bar')),
    ]

    assert remove_overlapping_marks(marks) == [marks[0]]
