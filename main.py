import fileinput
import glob
import os
import random

import time

import re

from arghandler import ArgumentHandler, subcmd
from google import search
from subprocess import call

from procurer import ultimate_guitar, lastfm, postulate_url
from rules import rules, clean
from songbook_converter import SongBook,  wrap, header
from writer import TexWriter, PdfWriter, FileWriter


def url(keyword):
    searchterm = "site:ultimate-guitar.com chords " + keyword
    results = search(searchterm, stop=10)
    for url in results:
        time.sleep(random.random())
        if 'search' not in url:
            return url
    raise ArithmeticError


import codecs


def filter_existing(lines):
    keywords = set(x for x in lines if not find_file_for_keyword(x))
    excluded = lines - keywords
    if excluded:
        print("Not adding some files ( use --force to override):")
        for item in excluded:
            print(item, find_file_for_keyword(item))
        print("Still looking for")
        for item in keywords:
            print(item, find_file_for_keyword(item))
    return keywords


def addsongs(keywords):
    written = []
    for line in keywords:
        try:
            source = url(line)
            artist, title, blob = ultimate_guitar(source)
            FileWriter(artist, title, blob, directory='raw/', extension='txt').write()
        except Exception as e:
            print("Couldn't add " + line)
            print(e)
            written.append(line)
    return written


def find_file_for_keyword(keyword):
    globs = (filename.split("\\")[-1][:-5] for filename in glob.glob('reviewed/**'))
    for filename in globs:
         if keyword.lower() in filename.lower():
             return True
         if filename.lower() in keyword.lower():
             return True
    return False


@subcmd
def edit(parser, context, args):
    matching_files = find_file_for_keyword("".join(args))
    if len(matching_files) == 1:
        call(["texmaker", matching_files[0]])


@subcmd
def add(parser, context, args):
    source = url(args)
    artist, title, blob = ultimate_guitar(source)
    FileWriter(artist, title, blob, directory='raw/', extension='txt').write()


@subcmd
def addfile(parser, context, args):
    lines = set(line.strip() for line in open(args[0]))
    if not "force" in args:
        keywords = filter_existing(lines)
    else:
        keywords = lines
    added = addsongs(keywords)
    with open("written.txt", "w") as f:
        f.writelines(added)


def files(directory):
    for file in glob.glob(directory + "*"):
        with codecs.open(file, encoding='utf-8')as f:
            artist, title = os.path.split(file)[-1][:-4].split(" - ")
            song = f.read()
        yield artist, title, song


@subcmd
def maketex(parser, context, args=('clean',)):
    if not len(args):
        args=('clean',)
    for artist, title, blob in files(args[0] + "/"):
        converter = SongBook(artist, title, blob)
        latex = converter.produce_song()
        TexWriter(artist, title, latex, directory="library/").write()


@subcmd
def cleanraw(parser, context, args=('raw',)):
    if not len(args):
        args = ('raw',)
    for artist, title, blob in files(args[0] + "/"):
        blob = clean(blob)
        if not "[" in blob:
            blob = "[Instrumental]\n" + blob
        FileWriter(artist, title, blob, directory='clean/', extension='txt').write()
    for artist, title, blob in files("clean/"):
        blob = clean(blob)
        if not "[" in blob:
            blob = "[Instrumental]\n" + blob
        FileWriter(artist, title, blob, directory='clean/', extension='txt').write()




@subcmd
def makepdf(parser, context, args=('library',)):
    if not len(args):
        args=('library',)
    latex = (line for line in fileinput.input(glob.glob(args[0] + '/*.tex'), openhook=fileinput.hook_encoded("utf-8")))
    latex = header() + wrap("document", "\n".join(latex))
    print([(sym,ord(sym)) for sym in latex if ord(sym)>1000])
    PdfWriter("Sebastian", "Songbook", latex).write()


@subcmd
def reviewtopdf(parser, context, args):
    print("Making tex")
    maketex(parser,context,('reviewed',))
    print("Making pdf")
    makepdf(parser,context,args=('library',))
if __name__ == "__main__":
    handler = ArgumentHandler()
    handler.run()
