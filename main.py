from itertools import zip_longest

from processing import symbolize
from latex import chord

def convert_chords(c,t):
    return symbolize(c), t
def separate_lines(blob):
    yield from zip(blob.splitlines()[::2], blob.splitlines()[1::2])

def process_verse(blob):
    res = [zip_longest(*convert_chords(*line), fillvalue=" ") for line in separate_lines(blob)]
    res = [[chord(a, b) if not a.isspace() else b for a, b in line] for line in res]
    return  "\n".join("".join(e) for e in res)
if __name__ == "__main__":
    pass

