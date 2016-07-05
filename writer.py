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
        if self.directory:
            call(['mkdir','-p',self.directory])

    @property
    def path(self):
        return self.directory + self.filename + "." + self.extension

    @property
    def filename(self): return " - ".join([self.artist.strip(), self.title.strip()])

    def write(self):
        import codecs
        print(".",end="",flush=True)
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
