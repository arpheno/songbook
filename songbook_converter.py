import re
from itertools import accumulate, zip_longest, chain

from converter import Converter
from processing import groupby_spaces, join_chord_and_leave_spaces, flatten, grouplines
from words import most_common


def chord(symbol, text):
    result = r"\Chr{%s}{%s}" % (symbol, text)
    return result


documentclass = r"""\documentclass[a5paper,8pt]{book}
\usepackage[chordbk]{songbook}

\usepackage{pgfpages}
\pgfpagesuselayout{2 on 1}[a4paper,landscape,border shrink=5mm]"""


def songbook_header():
    return documentclass + r'''\newcommand{\CCLInumber}{\#999999}
\newcommand{\CCLIed}{(CCLI \CCLInumber)}
\newcommand{\NotCCLIed}{}
\newcommand{\PGranted}{}
\newcommand{\PPending}{(Permission Pending)}
\makeTitleIndex
\makeTitleContents
\makeKeyIndex
\makeArtistIndex

'''


def extend_single_chords(symbols):
    skip = False
    for symbol in symbols:
        if not symbol.isspace() and len(symbol) == 1:
            yield symbol + " "
            skip = True
        if not skip:
            yield symbol
        else:
            skip = False


def symbolize(line_with_chords):
    grouped = groupby_spaces(line_with_chords)
    symbols = join_chord_and_leave_spaces(grouped)
    flat = flatten(symbols)
    symbols = extend_single_chords(flat)
    return symbols


def split_song(blob, grammar):
    parts = list(re.split(grammar, blob))
    parts = list(zip(parts[::2], parts[1::2]))
    return parts


def canonize_header(header):
    """
    >>> canonize_header('[verse 3]')
    '[SBVerse]'
    """
    sections = {
        'intro': '[SBIntro]',
        'verse': '[SBVerse]',
        'bridge': '[SBBridge]',
        'outro': '[SBEnd]',
        'chorus': '[SBChorus]',
    }
    for key in sections:
        if key in header.lower():
            return sections[key]
    return '[SBOpGroup]'


def wrap(header, section, *args):
    """
    >>> wrap('[SBVerse]',"x")
    '\\\\begin{SBVerse}\\nx\\\\end{SBVerse}\\n'
    """
    wrapper = header.strip("[]").strip()
    if args:
        section = "".join("{" + arg + "}" for arg in args) + '\n' + section
    return '\\begin{%s}\n%s\\end{%s}\n' % (wrapper, section, wrapper)


def convert_chords(c, t):
    result = list(symbolize(c))
    acc = 0, *list(accumulate(len(x) for x in result)), 999
    trans = [t[start:end] for start, end in zip(acc, acc[1:])]
    return result, trans


def bad_line(line):
    if "_" in line:
        return True
    return False


class SongBook(Converter):
    def __init__(self, artist, title, preformatted_song):
        self.title = title.replace("Chords", "")
        self.artist = artist
        self.blob = preformatted_song
        self.blob = "\n".join(line for line in self.blob.splitlines() if not bad_line(line))

    def is_chordline(self, line):
        keys = "CDFGBH"
        flatchords = [key + '#' for key in keys] + [key + 'b' for key in keys]
        mollchords = [a + 'm' for a in chain(keys, flatchords)]
        if any(x in line for x in chain(mollchords, flatchords)):
            return True
        if len([x for x in line if x.isspace()]) / len(line) > 0.3:
            return True
        return False

    def align_chords_and_text(self, section):
        """Returns tuples of lines of text. (Chordline,Lyricsline)"""
        result = []
        CHORD, LYRICS = 0, 1
        section = [line + " " for line in section.splitlines() if line]
        for line in section:
            if all(c.isspace() or not c for c in line):
                continue
            if any(word in line for word in most_common):
                result.append((LYRICS, line))
            elif self.is_chordline(line):
                result.append((CHORD, line))
            else:
                result.append((LYRICS, line))
        to_add, final = CHORD, []
        for line in result:
            if line[0] == to_add:
                final.append(line[1])
                to_add = (to_add + 1) % 2
            else:
                final.append(" ")
                final.append(line[1])
        if len(final) % 2:
            final.append(" ")
        return "\n".join(final)

    def process_verse(self, verse):
        aligned_verse = self.align_chords_and_text(verse)
        res = [convert_chords(*line) for line in grouplines(aligned_verse)]
        res = [zip_longest(chords, text, fillvalue=" ") for chords, text in res]
        res = [[chord(a, b) if not a.isspace() else b for a, b in line] for line in res]
        return "\n\n".join("".join(e) for e in res)

    def produce_song(self):
        sections = split_song(self.blob, r'(\[.*?\])')
        sections = [(canonize_header(header), self.process_verse(section)) for header, section in sections]
        asd = []
        for e in sections:
            if not e in asd:
                asd.append(e)
            else:
                asd.append((e[0], "Sing " + e[0][3:-1]))
        sections = [wrap(header, content) for header, content in asd]
        body = "\n".join(sections)
        body = body.replace("#", r"\#")
        song = wrap("song", body, self.title, "", self.artist, self.artist, "", "")
        return song

    def produce_songbook(self):
        song = self.produce_song()
        latex = songbook_header() + wrap("document", song)
        return latex
