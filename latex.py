def chord(symbol, text):
    result =  r"\Ch{%s}{%s}"% (symbol, text)
    return result
def songbook_header():
   return r'''\documentclass[12pt]{book}
\usepackage[chordbk]{songbook} %% Words & Chords edition.
%%
% C.C.L.I. license number definition; for copyright licensing info.
%%
\newcommand{\CCLInumber}{\#999999}
\newcommand{\CCLIed}{(CCLI \CCLInumber)}
\newcommand{\NotCCLIed}{}
\newcommand{\PGranted}{}
\newcommand{\PPending}{(Permission Pending)}
%%
% Turn on index and table of contents.
%%
\makeTitleIndex %% Title and First Line Index.
\makeTitleContents %% Table of Contents.
\makeKeyIndex %% Song Key Index.
\makeArtistIndex %% Index by Artist.
'''