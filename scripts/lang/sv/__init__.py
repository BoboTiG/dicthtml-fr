"""Swedish language."""

# Regex to find the pronunciation
pronunciation = r"{uttal\|sv\|(?:.+/([^/,]+)/.+|ipa=([^}]+))}"

# Regex to find the genre
genre = ""

# Markers for sections that contain interesting text to analyse.
# https://sv.wiktionary.org/wiki/Wiktionary:Stilguide#Ordklassrubriken
head_sections = ("Svenska",)
sections = (
    "Adjektiv",
    "Adverb",
    "Affix",
    "Artikel",
    "Efterled",
    "Förkortning",
    "Förled",
    "Interjektion",
    "Konjunktion",
    "Possessivt pronomen",
    "Postposition",
    "Prefix",
    "Preposition",
    "Pronomen",
    "Substantiv",
    "Suffix",
    "Verbpartikel",
)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = tuple()  # type: ignore

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep = tuple()  # type: ignore

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Templates to ignore: the text will be deleted.
templates_ignored = tuple()  # type: ignore

# Templates that will be completed/replaced using italic style.
templates_italic = {}  # type: ignore

# Templates more complex to manage.
templates_multi = {
    # {{avledning|sv|mälta|ordform=prespart}}
    "avledning": "f\"{italic('presensparticip av')} {parts[2]}\"",
    # {{tagg|historia}}
    # {{tagg|kat=nedsättande|text=något nedsättande}}
    "tagg": "term(tag(parts[1:]))",
    # {{uttal|sv|ipa=mɪn}}
    "uttal": "f\"{strong('uttal:')} /{parts[-1].lstrip('ipa=')}/\"",
}

# Templates that will be completed/replaced using custom style.
templates_other = {}  # type: ignore

# A warning will be printed when a template contains superfuous spaces,
# except for those listed bellow:
templates_warning_skip = ()

# Release content on gitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/sv
release_description = """\
Words count: {words_count}
Wiktionary dump: {dump_date}

:arrow_right: Download: [dicthtml-ca.zip]({url})

---

Installation:

1. Copy the `dicthtml-ca.zip` file into the `.kobo/dict/` folder of the reader.
2. Restart the reader.

---

Caracteristics :

- Only definitions are included: there is no quote nor ethymology.
- 1-character words are not included.
- Proper nouns are not included.
- Conjuged verbs are not included.

<sub>Updated on {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
