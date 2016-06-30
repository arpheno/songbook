import re

rules = {
    r"Verse \d:": "[Verse]",
    r"\[Verse \d\]": "[Verse]",
    r"Chours:": "[Chorus]",
    r"Intro:": "[Intro]",
    r"\[Refrain\]": "[Chorus]",
    r"Refren:": "[Chorus]",
    r"Bridge( \d)?:": "[Bridge]\n",
    r"Chorus( \d)?:": "[Chorus]\n",
    r"^Ref[:\.]": "[Chorus]",
    r'^(\s*)(\d)\.':'[Verse]\n\\1  ',
}
deletions = {
    r"\w\|+.*\|": "",
    r".*[Tt]abbed by.*": "",
    r".*[x\d]{6}.*": "",
    r"Tuning: .*": "",
    r"^Chords .*": "",
    r"^artist.*" :"",
    r"^title.*" :"",
    r"^band.*" :"",
    r"^song.*" :"",
    r"^timing.*" :"",
    r"^Words and Music by.*" :"",
    r"^Transcribed by.*" :"",
    r"^#.*" :"",
    r"^Standard Tuning":"",
    r"^=.*":"",
    r'[eBGDAE] .*--\d--.*':'',
    r'^[eBGDAE].*\|':'',
    r"^\|+.*\|$": "",
    r'.*@.*':'',
    r'.*visit my website.*':'',
    r'\*.*':'',
    r'.*http.*':'',
    r'%':'',
    r'let ring':'',
    r'^\(.*\)$':'',
    r'^[eBDGAE]$':'',
}
rules.update(deletions)

def clean(text):
    # Create a regular expression  from the dictionary keys
    result = []
    for line in text.splitlines():
        for pattern, replacement in rules.items():
            line = re.sub(pattern, replacement, line,flags=re.I)
        if not all(x.isspace() for x in line):
            result.append(line)
    return "\n".join(result)

