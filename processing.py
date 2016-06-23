from itertools import groupby


def flatten(l):
    yield from (item for sublist in l for item in sublist)


def groupby_spaces(line_with_chords):
    yield from (list(l) for k, l in groupby(line_with_chords, " ".__eq__))


def join_chord_and_leave_spaces(grouped):
    yield from (["".join(l)] if any(not e.isspace() for e in l) else l for l in grouped)


def grouplines(blob):
    yield from zip(blob.splitlines()[::2], blob.splitlines()[1::2])