from collections import defaultdict  # noqa
from typing import Dict, List, Tuple

from ...user_functions import extract_keywords_from, italic, strong, term
from .labels import label_syntaxes, labels


def render_forma(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_forma("forma-a", ["ca", "Candelera"], defaultdict(str))
    '<i>forma alternativa de</i> <b>Candelera</b>'
    >>> render_forma("forma-a", ["ca", "Candelera"], defaultdict(str, {"alt": "la Candelera"}))
    '<i>forma alternativa de</i> <b>la Candelera</b>'
    >>> render_forma("forma-a", ["mul", "I"], defaultdict(str, {"glossa": "1 en números romans"}))
    '<i>forma alternativa de</i> <b>I</b> («1 en números romans»)'
    """  # noqa
    forma = {
        "forma-": "forma abreujada de",
        "forma-a": "forma alternativa de",
        "forma-augm": "forma augmentativa de",
        "forma-dim": "forma diminutiva de",
        "forma-inc": "forma incorrecta de",
        "forma-pron": "forma pronominal de",
        "forma-super": "forma superlativa de",
    }[tpl]
    phrase = f"{italic(forma)} {strong(data['alt'] or parts[-1])}"
    if data["glossa"]:
        phrase += f" («{data['glossa']}»)"
    return phrase


def render_label(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_label("marca", ["ca", "castells"], defaultdict(str))
    '<i>(argot casteller)</i>'
    >>> render_label("marca", ["ca", "medicina"], defaultdict(str))
    '<i>(medicina)</i>'
    >>> render_label("marca", ["ca", "neologisme", "humorístic", "i", "a vegades", "despectiu"], defaultdict(str))
    '<i>(neologisme, humorístic i a vegades, despectiu)</i>'
    >>> render_label("marca", ["ca", "pronominal", "valencià", "_", "col·loquial"], defaultdict(str))
    '<i>(pronominal, valencià col·loquial)</i>'
    """  # noqa
    res = ""
    omit_preComma = False
    omit_postComma = True

    for label in parts[1:]:
        omit_preComma = omit_postComma
        omit_postComma = False

        syntax = label_syntaxes.get(label)
        omit_comma = omit_preComma or (syntax["omit_preComma"] if syntax else False)
        omit_postComma = syntax["omit_postComma"] if syntax else False

        if label_display := labels.get(label):
            if res:
                res += " " if omit_comma else ", "
            res += label_display
        elif label != "_":
            res += " " if omit_comma else ", "
            res += label

    return term(res.strip())


template_mapping = {
    "forma-": render_forma,
    "forma-a": render_forma,
    "forma-augm": render_forma,
    "forma-dim": render_forma,
    "forma-inc": render_forma,
    "forma-pron": render_forma,
    "forma-super": render_forma,
    "marca": render_label,
    "marca-nocat": render_label,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
