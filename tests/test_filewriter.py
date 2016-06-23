from writer import TexWriter


def test_filewriter_filename():
    assert TexWriter("a", "b", "").filename == "a - b"


def test_filewriter_extension():
    assert TexWriter("", "", "").extension == "tex"


def test_filewriter_path():
    assert TexWriter("a", "b", "").path == "a - b.tex"
