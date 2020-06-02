"""Internationalization stuff."""
import re

from . import ca, fr
from .fr.langs import langs as FR

# A list of all languages translated into different locales
all_langs = {
    "fr": FR,
}

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = {
    "ca": ca.definitions_to_ignore,
    "fr": fr.definitions_to_ignore,
}

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep = {
    "ca": ca.words_to_keep,
    "fr": fr.words_to_keep,
}

# Regex to find the pronunciation
pronunciation = {
    "ca": re.compile(ca.pronunciation),
    "fr": re.compile(fr.pronunciation),
}

# Regex to find the genre
genre = {
    "ca": re.compile(ca.genre),
    "fr": re.compile(fr.genre),
}

# Markers for sections that contain interesting text to analyse.
head_sections = {
    "ca": ca.head_sections,
    "fr": fr.head_sections,
}
sections = {
    "ca": ca.sections,
    "fr": fr.sections,
}

# The template name dealing with files in the Wikicode.
# [[Fichier:...|...|...|...]] (fr)
# [[File:...|...|...|...]] (fr)
# [[Fitxer:...|...|...]] (ca)
# [[Image:...|...|...]] (fr)
pattern_file = ("Fichier", "File", "Fitxer", "Image")

# Float number separator
float_separator = {
    "ca": ca.float_separator,
    "fr": fr.float_separator,
}

# Thousads separator
thousands_separator = {
    "ca": ca.thousands_separator,
    "fr": fr.thousands_separator,
}

# Templates replacements: wikicode -> text conversion

# Templates to ignore: the text will be deleted.
templates_ignored = {
    "ca": ca.templates_ignored,
    "fr": fr.templates_ignored,
}

# Templates that will be completed/replaced using italic style.
# Ex: {{absol}} -> <i>(Absolument)</i>
# Ex: {{absol|fr}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123|...}} -> <i>(Absolument)</i>
templates_italic = {
    "ca": ca.templates_italic,
    "fr": fr.templates_italic,
}

# Templates more complex to manage. More work is needed.
# The code on the right will be passed to a function that will execute it.
# It is possible to use any Python fonction and ones defined in user_functions.py.
#
# Available arguments:
#   - *tpl* (string) containing the template name.
#   - *parts* (list of strings) containing the all parts of the template.
#
# Example with the complete template "{{comparatif de|bien|fr|adv}}":
#   - *tpl* will contain the string "comparatif de".
#   - *parts* will contain the list ["comparatif de", "bien", "fr", "adv"].
#
# You can access to *tpl* and *parts* to apply changes and get the result wanted.
#
# Available functions are documented into that HTML file:
#   html/scripts/user_functions.html
templates_multi = {
    "ca": ca.templates_multi,
    "fr": fr.templates_multi,
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "ca": ca.templates_other,
    "fr": fr.templates_other,
}

# A warning will be printed when a template contains superfuous spaces,
# except for those listed bellow:
templates_warning_skip = {
    "ca": ca.templates_warning_skip,
    "fr": fr.templates_warning_skip,
}

# The full release description on GitHub:
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/$LOCALE
release_description = {
    "ca": ca.release_description,
    "fr": fr.release_description,
}

# Dictionary name that will be printed below each definition
wiktionary = {
    "ca": ca.wiktionary,
    "fr": fr.wiktionary,
}
