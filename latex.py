def chord(symbol, text):
    result =  r"\Ch{%s}{%s}"% (symbol, text)
    print(result)
    return result