from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "aberrasjon",
            [],
            ["m"],
            [
                "Fra latin <i>aberrātiō</i> («lindring, avvikelse») , fra <i>aberrō</i> («gå unna/bort, gå vill»), fra <i>ab</i> («bort») + <i>errō</i> («vandre/gå»).",
                "Se aberrate.",
            ],
            [
                "avvik, avvikelse",
                "<i>(astronomi)</i> avvik i en stjernes avbildede posisjon relativ til dens sanne posisjon.",
                "<i>(optikk)</i> avbildningsfeil i linser og speil.",
                "<i>(biologi)</i> endring i et kromosom mens celledeling pågår.",
            ],
            [],
        ),
        (
            "bare",
            [],
            [],
            [],
            [
                "begrensende, kun",
                "Gir dempende effekt",
                "Gir forsterkende effekt",
                "Gir en sitatfunksjon, særlig i muntlig språk.",
            ],
            ["bar"],
        ),
        (
            "funnet",
            [],
            [],
            [],
            [],
            ["finne", "funn"],
        ),
        (
            "konsentrasjon",
            [],
            ["m"],
            ["Fra <i>konsentrere</i> + -<i>sjon</i>"],
            [
                "Det å konsentrere seg; ha stort fokus på noe.",
                "<i>(kjemi)</i> Andelen stoff i noe; mengde stoff løst pr. enhet.",
            ],
            [],
        ),
        (
            "krokodille",
            [],
            ["m"],
            [
                "Fra middelalderlatin <i>cocodrillus</i> («krokodille»), fra gammelgresk κροκόδειλος (<i>krokodeilos</i>)"
            ],
            ["stort reptil, lever i og nær vann. <i>(lat. Crocodylia)</i>"],
            [],
        ),
        (
            "lumpen",
            [],
            [],
            [],
            ["tarvelig, nedrig"],
            ["lump"],
        ),
        (
            "seg",
            [],
            [],
            ["Av norrønt <i>sik</i>."],
            ["refleksivt pronomen, tredje person entall og flertall"],
            [],
        ),
        (
            "slå to fluer i en smekk",
            [],
            [],
            [],
            ["<i>(idiomatisk)</i> få gjort to ting med én handling"],
            [],
        ),
        (
            "tolvte",
            [],
            [],
            ["Fra norrønt <i>tolfti</i>; <i>tolv</i> + -<i>te</i>"],
            ["ordenstallet til tolv"],
            [],
        ),
        (
            "uten",
            [],
            [],
            [],
            ["som ikke har;som mangler"],
            [],
        ),
        (
            "verken",
            [],
            [],
            ["Fra gammeldansk: hwærki/hwærkin via dansk: hverken. Jamfør norrønt: hvárki."],
            ["danner sammen med eller en konjunksjon som binder sammen to nektinger"],
            ["verk"],
        ),
        (
            "Øyvind",
            [],
            [],
            [],
            ["Norsk mannsnavn"],
            [],
        ),
        (
            "ØNH",
            [],
            [],
            [],
            ["forkortelse for <i>øre-nese-hals</i>"],
            [],
        ),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: list[str],
    genders: list[str],
    etymology: list[Definitions],
    definitions: list[Definitions],
    variants: list[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "no")
    details = parse_word(word, code, "no", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{alternativ skrivemåte|be}}", "<i>alternativ skrivemåte av</i> <b>be</b>"),
        (
            "{{bøyningsform|no|sub|korp}}",
            "<i>bøyningsform av</i> <b>korp</b>",
        ),
        (
            "{{feilstaving av|førstvoterende|språk=no}}",
            "Feilstaving av førstvoterende.",
        ),
        ("{{l|no|god, snill}}", "god, snill"),
        ("{{opphav|norrønt|språk=no}}", "norrønt"),
        ("{{prefiks|a|biotisk|språk=no}}", "<i>a</i>- + <i>biotisk</i>"),
        ("{{qualifier|idiomatisk}}", "<i>(idiomatisk)</i>"),
        ("{{suffiks|konsentrere|sjon|språk=no}}", "<i>konsentrere</i> + -<i>sjon</i>"),
        (
            "{{tidligere bøyningsform|no|sub|jul}}",
            "<i>tidligere bøyningsform av</i> <b>jul</b>",
        ),
        (
            "{{tidligere skriveform|no|kunstnarleg}}",
            "<i>tidligere skriveform av</i> <b>kunstnarleg</b>",
        ),
        (
            "{{tidligere skrivemåte|no|naturlig tall}}",
            "<i>tidligere skriveform av</i> <b>naturlig tall</b>",
        ),
        ("{{urspråk|germansk|daigjōn}}", "urgermansk *daigjōn"),
        ("{{vokabular|overført}}", "<i>(overført)</i>"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "no") == expected
