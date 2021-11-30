"""Spanish language."""
from typing import List, Tuple

from .campos_semanticos import campos_semanticos

# Regex to find the pronunciation
pronunciation = r"fone=([^}\|\s]+)"

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{lengua|es}}",)
section_sublevels = (4, 3)
etyl_section = ["Etimología"]
sections = (
    "Abreviaturas",
    "Adjetivo",
    "{{abreviatura",
    "{{adjetivo",
    "{{adverbio",
    "{{artículo",
    "{{conjunción",
    *etyl_section,
    "{{interjección",
    "{{onomatopeya",
    "{{prefijo",
    "{{preposición",
    "{{pronombre",
    "{{sufijo|",
    "{{sustantivo",
    "{{verbo",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "antropónimo femenino",
    "antropónimo masculino",
    "apellido",
    "definición imprecisa",
    "definición impropia",
    "f.adj2",
    "f.s.p",
    "forma adjetivo",
    "forma adjetivo 2",
    "forma participio",
    "forma verbo",
    "marcar sin referencias",
    "participio",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "ampliable",
    "arcoiris",
    "catafijo",
    "cita requerida",
    "citarequerida",
    "clear",
    "definición imprecisa",
    "inflect.es.sust.invariante" "inflect.es.sust.reg",
    "marcar sin referencias",
    "picdic",
    "picdiclabel",
    "préstamo",
    "pron-graf",
    "sin referencias",
)

# Templates that will be completed/replaced using italic style.
# use capital letter first, if lower, then see lowercase_italic
templates_italic = {
    **campos_semanticos,
    "afectado": "Literario",
    "ciudades": "Geografía",
    "elevado": "Literario",
    "germanía": "Jergal",
    "jergal": "Jergal",
    "jerga": "Jergal",
    "literario": "Literario",
    "lunf": "Lunfardismo",
    "poético": "Literario",
    "regiones": "Geografía",
    "rpl": "Río de la Plata",
    "rur": "Rural",
    "slang": "Jergal",
}

# Templates more complex to manage.
templates_multi = {
    # {{adjetivo de sustantivo|el mundo árabe}}
    "adjetivo de sustantivo": '"Que pertenece o concierne " + (f"{parts[2]} " if len(parts) > 2 else "a ") + f"{parts[1]}"',  # noqa
    # {{adjetivo de padecimiento|alergia}}
    "adjetivo de padecimiento": 'f"Que padece o sufre de {parts[1]}" + (f" o {parts[2]} " if len(parts) > 2 else "")',  # noqa
    # {{color|#DDB88E|espacio=6}}
    "color": "color([p for p in parts if '=' not in p][1] if len(parts) > 1 else '#000000')",
    # {{contexto|Educación}}
    "contexto": "term(lookup_italic(parts[-1], 'es'))",
    # {{contracción|de|ellas|leng=es}}
    "contracción": "f\"{italic('Contracción de')} {parts[1]} {italic('y')} {parts[2]}\"",
    # {{coord|04|39|N|74|03|O|type:country}}
    "coord": "coord(parts[1:])",
    # {{datación|xv}}
    "datación": 'f"Atestiguado desde el siglo {parts[-1]}"',
    # {{DRAE}}
    "DRAE": 'f"«{word}», <i>Diccionario de la lengua española (2001)</i>, 22.ª ed., Madrid: Real Academia Española, Asociación de Academias de la Lengua Española y Espasa."',  # noqa
    "DRAE2001": 'f"«{word}», <i>Diccionario de la lengua española (2001)</i>, 22.ª ed., Madrid: Real Academia Española, Asociación de Academias de la Lengua Española y Espasa."',  # noqa
    # {{etimología2|de [[hocicar]]}}
    "etimología2": "capitalize(parts[1]) if (len(parts) > 1 and parts[1] != '...') else ''",
    # {{formatnum:22905}}
    "formatnum": f'number(parts[1], "{float_separator}", "{thousands_separator}")',
    # {{impropia|Utilizado para especificar...}}
    "impropia": "italic(parts[1])",
    # {{nombre científico}}
    "nombre científico": "superscript(tpl)",
    # {{plm}}
    # {{plm|cansado}}
    "plm": "capitalize(parts[1] if len(parts) > 1 else word)",
    # {{redirección suave|protocelta}}
    "redirección suave": "f\"{italic('Véase')} {parts[1]}\"",
    # {{-sub|4}}
    "-sub": "subscript(parts[1])",
    # {{subíndice|5}}
    "subíndice": "subscript(parts[1])",
    # {{-sup|2}}
    "-sup": "superscript(parts[1])",
    # {{trad|la|post meridem}}
    "trad": 'f"{parts[2]}" + superscript(f"({parts[1]})")',
    # {{ucf|mujer}}
    "ucf": "capitalize(parts[1])",
    # {{variante obsoleta|hambre}}"
    "variante obsoleta": "f\"{italic('Variante obsoleta de')} {parts[1]}\"",
    # {{versalita|xx}}
    "versalita": "small_caps(parts[1])",
    # {{verde|*exfollare}}
    "verde": "italic(parts[1])",
}

lowercase_italic = ("Rural", "Jergal", "Lunfardismo")


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["Arqueología"], "es")
        '<i>(Arqueología)</i>'
        >>> last_template_handler(["Anatomía", "y" , "Zootomía"], "es")
        '<i>(Anatomía y Zootomía)</i>'
        >>> last_template_handler(["Angiología", "Endocrinología" , "Fisiología", "Medicina"], "es")
        '<i>(Angiología, Endocrinología, Fisiología, Medicina)</i>'
        >>> last_template_handler(["moluscos", "y" , "alimentos"], "es")
        '<i>(Zoología y Gastronomía)</i>'
        >>> last_template_handler(["cultura", "historia", "y", "lingüística"], "es")
        '<i>(Cultura, Historia y Lingüística)</i>'
        >>> last_template_handler(["Arte", "," , "Arquitectura"], "es")
        '<i>(Arte, Arquitectura)</i>'
        >>> last_template_handler(["Botánica", "leng=es"], "es")
        '<i>(Botánica)</i>'
        >>> last_template_handler(["deporte", "nota=fútbol"], "es")
        '<i>(Deporte (fútbol))</i>'
        >>> last_template_handler(["Fonética", "Fonética"], "es")
        '<i>(Lingüística (fonética), Fonética)</i>'
        >>> last_template_handler(["rur"], "es")
        '<i>(Rural)</i>'
        >>> last_template_handler(["rur", "deporte"], "es")
        '<i>(Rural, Deporte)</i>'
        >>> last_template_handler(["deporte", "rur"], "es")
        '<i>(Deporte, rural)</i>'
        >>> last_template_handler(["default"], "es")
        '<i>(Default)</i>'

        >>> last_template_handler(["variantes", "adestrador", "nota=poco frecuente"], "es")
        '<b>Variante:</b> adestrador (poco frecuente)'

        >>> last_template_handler(["en"], "es")
        'Inglés'
    """
    from ...user_functions import (
        capitalize,
        concat,
        extract_keywords_from,
        italic,
        lookup_italic,
        strong,
    )
    from .template_handlers import render_template, lookup_template
    from ..defaults import last_template_handler as default

    if lookup_template(template[0]):
        return render_template(template)

    if lookup_italic(template[0], locale, empty_default=True):
        tpl, *parts = template
        data = extract_keywords_from(parts)
        phrase = ""
        phrase_a: List[str] = []
        parts.insert(0, tpl)
        added = set()
        append_to_last = False
        for index, part in enumerate(parts, 1):
            sindex = str(index) if index > 1 else ""
            if part == ",":
                continue
            elif part in ("y", "e", "o", "u"):
                phrase_a[-1] += f" {part} "
                append_to_last = True
                continue
            else:
                local_phrase = lookup_italic(part, locale)
                if local_phrase not in added:
                    added.add(local_phrase)
                    if data["nota" + sindex]:
                        local_phrase += f' ({data["nota"+sindex]})'
                else:
                    local_phrase = part
            # some italic templates are in lower case if after the first one...
            if index > 1 and local_phrase in lowercase_italic:
                local_phrase = local_phrase.lower()
            if append_to_last:
                phrase_a[-1] += local_phrase
                append_to_last = False
            else:
                phrase_a.append(local_phrase)
        if phrase_a:
            phrase = italic(f'({concat(phrase_a, ", ")})')
        return phrase

    if template[0] == "variantes":
        _, *parts = template
        data = extract_keywords_from(parts)
        phrase = f"{strong('Variante:')} {parts[0]}"
        if data["nota"]:
            phrase += f" ({data['nota']})"
        return phrase

    from .langs import langs

    lang = langs.get(template[0])
    if lang:
        return capitalize(lang)

    return default(template, locale, word)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/es
release_description = """\
Número de palabras: {words_count}
exportación Wikcionario: {dump_date}

Archivos disponibles:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Actualizado el {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikcionario (ɔ) {year}"
