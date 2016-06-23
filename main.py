from itertools import zip_longest, accumulate

from processing import symbolize, ultimate_guitar, canonize_header, split_song, wrap
from latex import chord, songbook_header


def convert_chords(c, t):
    result = list(symbolize(c))
    acc = 0, *list(accumulate(len(x) for x in result)),999
    trans = [t[start:end] for start,end in zip(acc,acc[1:])]
    print(result)
    print(trans)
    return result, trans


def separate_lines(blob):
    yield from zip(blob.splitlines()[::2], blob.splitlines()[1::2])


def process_verse(blob):
    res = [zip_longest(*convert_chords(*line), fillvalue=" ") for line in separate_lines(blob)]
    res = [[chord(a, b) if not a.isspace() else b for a, b in line] for line in res]
    return "\n\n".join("".join(e) for e in res)


if __name__ == "__main__":
    one_call = 'https://tabs.ultimate-guitar.com/c/charlie_puth/one_call_away_crd.htm'
    wonderwall="https://tabs.ultimate-guitar.com/o/oasis/wonderwall_ver2_crd.htm"
    title, artist, song = ultimate_guitar(wonderwall)
    sections = split_song(song, r'(\[.*?\])')
    sections = [(canonize_header(header), process_verse(content)) for header, content in sections]
    sections = [wrap(header, content) for header, content in sections]
    body = "\n".join(sections)
    latex = songbook_header()+wrap("document",wrap("song", body, title, "", artist, artist, "", ""))
    with open(" - ".join([artist,title])+".tex","w") as f:
        f.write(latex)
