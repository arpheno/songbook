import shutil
from shlex import quote
from subprocess import call


class FileWriter(object):
    def __init__(self, title, artist, blob):
        self.title = title
        self.artist = artist
        self.blob = blob
        self.directory = ""
        self.extension = ""

    @property
    def path(self):
        return self.directory + self.filename + "." + self.extension

    @property
    def filename(self): return " - ".join([self.artist, self.title])

    def write(self):
        print("Writing file", self.path)
        with open(self.path, "w") as f:
            f.write(self.blob)


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
