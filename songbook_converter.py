import re
from itertools import accumulate, zip_longest

from converter import Converter
from processing import groupby_spaces, join_chord_and_leave_spaces, flatten, grouplines


def chord(symbol, text):
    result = r"\Ch{%s}{%s}" % (symbol, text)
    return result


documentclass = r"""\documentclass[a5paper,10pt]{article}
\usepackage[chordbk]{songbook}

\usepackage{pgfpages}                                 % <— load the package
\pgfpagesuselayout{2 on 1}[a4paper,landscape,border shrink=5mm] %%"""


def songbook_header():
    return documentclass+r'''\newcommand{\CCLInumber}{\#999999}
\newcommand{\CCLIed}{(CCLI \CCLInumber)}
\newcommand{\NotCCLIed}{}
\newcommand{\PGranted}{}
\newcommand{\PPending}{(Permission Pending)}
%%
% Turn on index and table of contents.
%%
\makeTitleIndex %% Title and First Line Index.
\makeTitleContents %% Table of Contents.
\makeKeyIndex %% Song Key Index.
\makeArtistIndex %% Index by Artist.
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
    parts = re.split(grammar, blob)[1:]  # Element 0 is empty
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
            print(sections[key])

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
    print(result)
    print(trans)
    return result, trans


class SongBook(Converter):
    def __init__(self, title, artist, preformatted_song):
        self.title = title
        self.artist = artist
        self.blob = preformatted_song

    def process_verse(self, verse):
        res = [convert_chords(*line) for line in grouplines(verse)]
        res = [zip_longest(chords, text, fillvalue=" ") for chords, text in grouplines(verse)]
        res = [[chord(a, b) if not a.isspace() else b for a, b in line] for line in res]
        return "\n\n".join("".join(e) for e in res)

    def produce_songbook(self):
        sections = split_song(self.blob, r'(\[.*?\])')
        sections = [(canonize_header(header), self.process_verse(section)) for header, section in sections]
        sections = [wrap(header, content) for header, content in sections]
        body = "\n".join(sections)
        song = wrap("song", body, self.title, "", self.artist, self.artist, "", "")
        latex = songbook_header() + wrap("document", song)
        return latex
