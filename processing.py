import re
from itertools import groupby

from bs4 import BeautifulSoup
from requests import get


def flatten(l):
    yield from (item for sublist in l for item in sublist)


def groupby_spaces(line_with_chords):
    yield from (list(l) for k, l in groupby(line_with_chords, " ".__eq__))


def join_chord_and_leave_spaces(grouped):
    yield from (["".join(l)] if any(not e.isspace() for e in l) else l for l in grouped)


def extend_single_chords(symbols):
    skip = False
    for symbol in symbols:
        if not symbol.isspace() and len(symbol)==1:
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


def ultimate_guitar(url):
    content = get(url).content
    soup = BeautifulSoup(content, "html.parser")
    return soup.h1.text, soup.find("div", {"class": "t_autor"}).a.text, soup.find_all("pre")[-1].text
