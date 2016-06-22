from main import process_verse


def test_process_verse():
    test = '''\
          C   G    Am7
I'm only one call away
                  F   Am7   G
I'll be there to save the day
              C   G     Am7
Superman got nothing on me
          F   Dm   C
I'm only one call away'''
    expected = '''\
I'm only o\Ch{C}{n}e c\Ch{G}{a}ll a\Ch{Am7}{w}ay
I'll be there to s\Ch{F}{a}ve \Ch{Am7}{t}he \Ch{G}{d}ay
Superman got n\Ch{C}{o}thi\Ch{G}{n}g on \Ch{Am7}{m}e
I'm only o\Ch{F}{n}e c\Ch{Dm}{a}ll \Ch{C}{a}way'''
    assert process_verse(test) == expected
