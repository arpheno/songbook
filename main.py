import fileinput
import glob
import random

import time

import re
from arghandler import ArgumentHandler, subcmd
from google import search
from subprocess import call

from procurer import ultimate_guitar, lastfm, postulate_url
from rules import rules, clean
from songbook_converter import SongBook, songbook_header, wrap
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
    return [filename for filename in glob.glob('library/**') if keyword.lower() in filename.lower()]


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
            artist, title = file.split("/")[-1][:-4].split(" - ")
            song = f.read()
        yield artist, title, song


@subcmd
def maketex(parser, context, args):
    for artist, title, blob in files("clean/"):
        converter = SongBook(artist, title, blob)
        latex = converter.produce_song()
        TexWriter(artist, title, latex, directory="library/").write()


@subcmd
def cleanraw(parser, context, args):
    for artist, title, blob in files("raw/"):
        blob = clean(blob)
        if not "[" in blob:
            blob = "[Instrumental]\n" + blob
        FileWriter(artist, title, blob, directory='clean/', extension='txt').write()

@subcmd
def sanitize(parser, context, args):
    result = []
    for line in open(args[0]):
        artist, title = lastfm(line.strip())
        if artist and title and not find_file_for_keyword(artist + ' - '+ title):
            result.append(artist+" - "+title)
        else:
            result.append(line)
    with open("sanitized.txt",'w') as f:
        f.writelines(result)



def asdasdas(parser, context, args):
    for line in open(args[0]):
        source = postulate_url(*lastfm(line.strip()))
        print(source)
        artist, title, blob = ultimate_guitar(source)
        FileWriter(artist, title, blob, directory='raw/', extension='txt').write()


@subcmd
def makepdf(parser, context, args):
    latex = (line for line in fileinput.input(glob.glob("library/*.tex"), openhook=fileinput.hook_encoded("utf-8")))
    latex = songbook_header() + wrap("document", "\n".join(latex))
    PdfWriter("Sebastian", "Songbook", latex).write()


if __name__ == "__main__":
    handler = ArgumentHandler()
    handler.run()
