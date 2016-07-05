import fileinput
import glob
import re
from itertools import accumulate, zip_longest, chain
from string import punctuation

from converter import Converter
from processing import groupby_spaces, join_chord_and_leave_spaces, flatten, grouplines
from rules import clean
from words import keysigns
from words import most_common


def chord(symbol, text):
    result = r"\Chr{%s}{%s}" % (symbol, text)
    return result


def header():
    """ Return everything from latex/ line by line starting with _documentclass"""
    files = ["latex/documentclass.tex"] + glob.glob("latex//my**")
    print(files)
    return "".join(line for line in fileinput.input(files))


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
    parts = list(re.split(grammar, blob))[1:]
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
        'pre-chorus': '[SBPrechorus]',
        'instrumental': '[SBInstrumental]',
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


def is_chordline(line):
    keys = "CDFGBEHA"
    flatchords = [key + '#' for key in keys] + [key + 'b' for key in keys]
    chords=list(chain(keys, flatchords))
    mollchords = [a + 'm' for a in chords]
    majchords = [key+x for key in chords for x in ["maj7","min","Min"]]
    powerchords = [key+x for key in chain(mollchords,chords) for x in "576"]
    suschords=[key+'sus'+x for key in chain(mollchords,chords,powerchords) for x in "24"]
    addchords=[key+'add'+x for key in chain(mollchords,chords) for x in ["7","9",'11','13']]
    whitespace = ["\w.*\s\s"]
    import re
    myregex = "|".join(r"^.*" + x + r"(\*)?\s.*$" for x in chain(keys, powerchords,mollchords, flatchords,suschords,majchords,addchords))
    chords = re.compile(myregex)
    return chords.match(line)
def is_lyricsline(line):
    if any(x in line for x in keysigns):
        return True
    line = [word.lower().strip(punctuation) for word in line.split()]
    if any(word in  line for word in most_common):
        return True

def multireplace(text, rep):
    import re
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


class SongBook(Converter):
    post_processing_rules = {
            "#": r"\#",
            "&": r"\&",
            "\xa0": r" ",
            chr(8216): r"'",
            chr(8217): r"'",
            chr(8211): r"-",
            chr(8222): r'"',
            chr(8221): r'"',
            chr(8230): r"...",
        }
    def __init__(self, artist, title, preformatted_song):

        self.title = title.replace("Chords", "")
        self.artist = artist
        self.blob = preformatted_song

    def pre_processing_replace(self):
        self.blob = re.sub("[{}]", "", self.blob)
        self.blob = "\n".join(line for line in self.blob.splitlines() if not bad_line(line))

    def align_chords_and_text(self, section):
        """Returns tuples of lines of text. (Chordline,Lyricsline)"""
        result = []
        CHORD, LYRICS = 0, 1
        section = [line + " " for line in section.splitlines() if line]
        for line in section:
            if all(c.isspace() or not c for c in line):
                continue
            elif is_lyricsline(line):
                result.append((LYRICS, line))
            elif is_chordline(line):
                result.append((CHORD, line))
            else:
                print("Couldn't identify ", line,". Guessing Lyrics")
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

    def post_processing_replace(self):
        self.body = multireplace(self.body, self.post_processing_rules)
    def produce_song(self):
        self.pre_processing_replace()
        sections = split_song(self.blob, r'(\[.*?\])')
        sections = [(canonize_header(header), self.process_verse(section)) for header, section in sections]
        asd = []
        for e in sections:
            if not e in asd:
                asd.append(e)
            else:
                asd.append((e[0], "Sing " + e[0][3:-1]))
        sections = [wrap(header, content) for header, content in asd]
        # body = clean(body, unicode_to_latex)
        self.body = "\n".join(sections)
        self.post_processing_replace()
        song = r'\CBPageBrk' + wrap("song", self.body, self.title, "", self.artist.replace(r"&", "r\&"),
                                    self.artist.replace(r"&", "r\&"), "", "")
        return song

    def produce_songbook(self):
        song = self.produce_song()
        latex = header() + wrap("document", song)
        return latex
