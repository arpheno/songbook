import shutil
from shlex import quote
from subprocess import call


class FileWriter(object):
    def __init__(self, artist,title, blob, extension="", directory=""):
        self.title = title.replace("Chords", '')
        self.artist = artist
        self.blob = blob
        self.directory = directory
        self.extension = extension

    @property
    def path(self):
        return self.directory + self.filename + "." + self.extension

    @property
    def filename(self): return " - ".join([self.artist, self.title])

    def write(self):
        import codecs
        print("Writing file", self.path)
        with codecs.open(self.path, "w", encoding="utf-8") as f:
            f.write(self.blob)
        return self.filename


class TexWriter(FileWriter):
    def __init__(self, *args, **kwargs):
        super(TexWriter, self).__init__(*args, **kwargs)
        self.extension = "tex"


class PdfWriter(TexWriter):
    def __init__(self, *args, **kwargs):
        super(PdfWriter, self).__init__(*args, **kwargs)
        self.library = "library/"
        self.auxiliary = "auxiliary/"

    def write(self):
        super(PdfWriter, self).write()
        args = ["--aux-directory=" + self.auxiliary, ]
        call([shutil.which("pdflatex"), self.path] + args)
