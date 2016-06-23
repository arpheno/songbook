from itertools import groupby

from bs4 import BeautifulSoup
from requests import get


def flatten(l):
    yield from (item for sublist in l for item in sublist)


def groupby_spaces(line_with_chords):
    yield from (list(l) for k, l in groupby(line_with_chords, " ".__eq__))


def join_chord_and_leave_spaces(grouped):
    yield from (["".join(l)] if any(not e.isspace() for e in l) else l for l in grouped)


def ultimate_guitar(url):
    content = get(url).content
    soup = BeautifulSoup(content, "html.parser")
    return soup.h1.text, soup.find("div", {"class": "t_autor"}).a.text, soup.find_all("pre")[-1].text


def grouplines(blob):
    yield from zip(blob.splitlines()[::2], blob.splitlines()[1::2])