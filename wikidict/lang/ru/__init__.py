"""Russian language."""
import re
from typing import Pattern, Tuple

from ...stubs import Pronunciations

# Regex to find the gender
# https://ru.wiktionary.org/wiki/%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD:%D1%81%D1%83%D1%89-ru
gender = r"(?:{сущ.ru.)([fmnмжс])|(?:{сущ.ru.*\|)([fmnмжс])"

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
section_level = 1
section_sublevels = (3, 4)
head_sections = "{{-ru-}}"
etyl_section = ("Этимология",)
sections = (
    *etyl_section,
    "Значение",
    "Семантические свойства",
    "{{Значение}}",
    "{{Семантические свойства}}",
    "Морфологические и синтаксические свойства",
    "Как самостоятельный глагол",  # for verbs with aux
    "В значении вспомогательного глагола или связки",  # for verbs with aux
)

# Some definitions are not good to keep (plural, gender, ... )
templates_ignored = ("семантика",)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ru
release_description = """\
Количество слов : {words_count}
Экспорт Викисловаря : {dump_date}

Доступные файлы :

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Обновлено по {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Викисловарь (ɔ) {year}"


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"(?:transcriptions-ru.)(\w*)"),
) -> Pronunciations:
    return list(set(pattern.findall(code)))


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:

    from ..defaults import last_template_handler as default
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(template)

    tpl, *parts = template

    # This is a country in the current locale
    return langs[tpl] if tpl in langs else default(template, locale, word=word)
