import argparse
import fileinput
import glob

from arghandler import ArgumentHandler, subcmd
from google import search

from procurer import ultimate_guitar
from songbook_converter import SongBook, songbook_header, wrap
from writer import TexWriter, PdfWriter


@subcmd
def add(parser, context, args):
    results = search("site:ultimate-guitar.com chords " + " ".join(args), stop=5)
    urls = [url for url in results if 'search' not in url]
    title, artist, song = ultimate_guitar(urls[0])
    converter = SongBook(title, artist, song)
    latex = converter.produce_song()
    writer = TexWriter(title, artist, latex)
    writer.directory = "library/"
    writer.write()


@subcmd
def create(parser, context, args):
    latex = (line for line in fileinput.input(glob.glob("library/*.tex")))
    latex = songbook_header() + wrap("document", "\n".join(latex))
    writer = PdfWriter("songbook", "a", latex)
    writer.write()


if __name__ == "__main__":
    handler = ArgumentHandler()
    handler.set_subcommands({'add': add, 'create': create})
    handler.run()
    one_call = 'https://tabs.ultimate-guitar.com/c/charlie_puth/one_call_away_crd.htm'
    wonderwall = "https://tabs.ultimate-guitar.com/o/oasis/wonderwall_ver2_crd.htm"
