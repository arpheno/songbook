from songbook_converter import is_chordline


def test_is_chordline_default():
    assert is_chordline("Am              G\n")
def test_is_chordline_single_chord():
    assert is_chordline("Am\n")
def test_is_chordline_two_close_chords():
    assert is_chordline("Am Am\n")
def test_is_chordline_notfirst():
    assert is_chordline(" Am\n")
def test_is_chordline_strange():
    assert is_chordline('    Em \n')
    assert is_chordline( '        Am    D   Em\n' )
def test_not_is_chordline_am():
    assert not is_chordline("Drowning in Amsterdam \n")
    assert not is_chordline("    Ich vermisse dich schon jetzt. ")
    assert not is_chordline('Whisky moja żono, jednak tyś najlepszą z dam')
    assert not is_chordline("Kiepski byłby mąż	  } x2")
