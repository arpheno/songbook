from processing import ultimate_guitar
from songbook_converter import SongBook
from writer import TexWriter, PdfWriter

if __name__ == "__main__":
    one_call = 'https://tabs.ultimate-guitar.com/c/charlie_puth/one_call_away_crd.htm'
    wonderwall = "https://tabs.ultimate-guitar.com/o/oasis/wonderwall_ver2_crd.htm"
    title, artist, song = ultimate_guitar(wonderwall)
    converter = SongBook(title, artist, song)
    latex = converter.produce_songbook()
    writer = PdfWriter(title, artist, latex)
    writer.write()

