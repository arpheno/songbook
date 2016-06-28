import re

rules = {
    r"Verse \d:": "[Verse]",
    r"Chours:": "[Chorus]",
    r"Intro:": "[Intro]",
    r"[Refrain]": "[Chorus]",
    r"[refrain]": "[Chorus]",
    r"Refren:": "[Chorus]",
    r"refren:": "[Chorus]",
}
deletions = {
    r"\w|+.*|": "",
    r".*[Tt]abbed by.*": "",
    r".*\d\d\d\d\d\d.*": "",
    r"Tuning: .*": "",
    r"Chords used:": "",
}
rules.update(deletions)
def clean(text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, rules.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: rules[mo.string[mo.start():mo.end()]], text)
