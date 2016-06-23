import shutil
from shlex import quote
from subprocess import call


class FileWriter(object):
    def __init__(self, title, artist, blob):
        self.title = title
        self.artist = artist
        self.blob = blob

    @property
    def path(self):
        return self.directory + self.filename + "." + self.extension

    @property
    def extension(self): return ""

    @property
    def directory(self): return ""

    @property
    def filename(self): return " - ".join([self.artist, self.title])

    def write(self):
        print("Writing file",self.path)
        with open(self.path, "w") as f:
            f.write(self.blob)


class TexWriter(FileWriter):
    @property
    def extension(self): return "tex"


class PdfWriter(TexWriter):

    def write(self):
        super(PdfWriter, self).write()
        call(["ls",'-l'])
        call([shutil.which("pdflatex"),'"'+self.path+'"'],shell=True)
