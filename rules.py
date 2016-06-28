import re

rules = {
    r"Verse \d:": "[Verse]",
    r"Chours:": "[Chorus]",
    r"[Rr]efrain": "[Chorus]",
    r"[Rr]efren": "[Chorus]",
}
deletions = {
    r"\w|+.*|": "",
    r".*[Tt]abbed by.*": "",
    r".*\d\d\d\d\d\d.*": "",
    r"Tuning: .*": "",
    r"Chords used:": "",
}
rules.update(deletions)
