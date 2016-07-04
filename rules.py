import re


def grammar():
    keywords = ['Intro', 'Pre-Chorus','Bridge', 'Chorus', 'Verse', 'Interlude', 'Instrumental', 'Break', 'Ending']
    patterns = {
        r"^KEYWORD": "[KEYWORD]",
        r"^KEYWORD": "[KEYWORD]",
        r".*\[KEYWORD": "[KEYWORD]",
    }
    return {k.replace('KEYWORD', x)+r'.*': v.replace('KEYWORD', x) for k, v in patterns.items() for x in keywords}

for k,v in grammar().items():
    print(k,v)
rules = {
    # Spelling
    r"Uvod": "Intro",
    r"verz": "Verse",
    r"Chours": "Chorus",
    r"^Chorus.*": "Chorus",
    r"Refren.*": "Chorus",
    r"Refrain.*": "Chorus",
    r"^Ref[:\.]": "Chorus",
    r"Coda": "Ending",
    r"Outro": "Ending",
    r"ZAKLJUČEK": "Ending",

    # Canon
    r'\[Chorus:? x?\d\]': '[Chorus]',
    r'^(\s*)(\d)\.': '[Verse]\n\\1  ',
    r'^I+:': 'Verse',
    r'fis': 'F#m',
}
rules.update(grammar())
capo  = {
    "^Capo.*(\d).*":"Capo \\1",
    ".*No Capo.*":"",
}
rules.update(capo)
deletions = {
    r"\w?\|+.*": "",
    r".*[Tt]abbed by.*": "",
    r".*[x\d]{6}.*": "",
    r"Tuning: .*": "",
    r"^Chords .*": "",
    r"^art?ist.*": "",
    r"^album.*": "",
    r"^title.*": "",
    r"^band.*": "",
    r"^song.*": "",
    r"^timing.*": "",
    r"^Words and Music by.*": "",
    r"^Transcribed by.*": "",
    r"^#.*": "",
    r"^Standard Tuning": "",
    r"^=.*": "",
    r'[eBGDAE] .*--\d--.*': '',
    r'^[eBGDAE].*\|': '',
    r"^\|+.*\|$": "",
    r'.*@.*': '',
    r'.*visit my website.*': '',
    r'\*.*': '',
    r'.*http.*': '',
    r'%': '',
    r'let ring': '',
    r'^\(.*\)$': '',
    r'^[eBDGAE]$': '',
    r'^--.*--': '',
    r'^-.*-': '',
    r'^by .*':'',
    r'^\.*': '',
    '\| h  Hammer-on': '',
    '\| p  Pull-off': '',
}
rules.update(deletions)


def clean(text):
    # Create a regular expression  from the dictionary keys
    result = []
    for line in text.splitlines():
        for pattern, replacement in rules.items():
            line = re.sub(pattern, replacement, line, flags=re.I)
        if not all(x.isspace() for x in line):
            result.append(line)
    return "\n".join(result)
