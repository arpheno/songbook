from itertools import zip_longest, accumulate, chain

from pyphen import Pyphen

from processing import symbolize, ultimate_guitar, canonize_header, split_song, wrap, flatten
from latex import chord, songbook_header


def convert_chords(c, t):
    result = list(symbolize(c))
    acc = 0, *list(accumulate(len(x) for x in result)), 999
    dic = Pyphen(lang='en_US')
    temp = list(flatten(dic.inserted(w).split("-") for w in t.split()))
    asd = 0,*[y+2 for y in accumulate(len(x) for x in temp)]
    csa = [(a, b) for a, b in zip(acc, result) if not b.isspace()]
    print(csa)
    aaa=list(zip(asd, temp))
    print(sorted(chain(aaa,csa)))
    dsa = [" " for x in temp]

    print(asd)
    trans = [t[start:end] for start, end in zip(acc, acc[1:])]
    return result, trans


def separate_lines(blob):
    yield from zip(blob.splitlines()[::2], blob.splitlines()[1::2])


def process_verse(blob):
    res = [zip_longest(*convert_chords(*line), fillvalue=" ") for line in separate_lines(blob)]
    res = [[chord(a, b) if not a.isspace() else b for a, b in line] for line in res]
    return "\n\n".join("".join(e) for e in res)


if __name__ == "__main__":
    one_call = 'https://tabs.ultimate-guitar.com/c/charlie_puth/one_call_away_crd.htm'
    wonderwall = "https://tabs.ultimate-guitar.com/o/oasis/wonderwall_ver2_crd.htm"
    title, artist, song = ultimate_guitar(wonderwall)
    sections = split_song(song, r'(\[.*?\])')
    sections = [(canonize_header(header), process_verse(content)) for header, content in sections]
    sections = [wrap(header, content) for header, content in sections]
    body = "\n".join(sections)
    latex = songbook_header() + wrap("document", wrap("song", body, title, "", artist, artist, "", ""))
    with open(" - ".join([artist, title]) + ".tex", "w") as f:
        f.write(latex)
