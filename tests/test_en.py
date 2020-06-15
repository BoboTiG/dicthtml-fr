import pytest

from scripts.get import parse_word
from scripts.utils import clean


@pytest.mark.parametrize(
    "word, pronunciation, genre, definitions",
    [
        (
            "ab",
            "æb",
            "",
            [
                "<i>(informal)</i> abdominal muscle. <small>[Mid 20<sup>th</sup> century.]</small>",
                "<i>(slang)</i> An abscess caused by injecting an illegal drug, usually heroin.",
                "<i>(climbing, informal)</i> To abseil.",
                "<i>Abbreviation of</i> <b>abort</b>",
                "<i>Abbreviation of</i> <b>abortion</b>",
                "<i>Abbreviation of</i> <b>about</b>",
                "<i>(US)</i> The early stages of; the beginning process; the start.",
            ],
        ),
        (
            "cum",
            "kʌm",
            "",
            [
                "<i>Used in indicating a thing with two roles, functions, or natures, or a "
                "thing that has changed from one to another.</i>",
                "<i>Used in indicating a thing with two or more roles, functions, or "
                "natures, or a thing that has changed from one to another.</i>",
                "<i>(slang, vulgar)</i> Semen.",
                "<i>(slang, vulgar)</i> Female ejaculatory discharge.",
                "<i>(slang, vulgar)</i> An ejaculation.",
                "<i>(slang)</i> To have an orgasm, to feel the sensation of an orgasm.",
                "<i>(slang)</i> To ejaculate.",
            ],
        ),
        (
            "efficient",
            "ɪˈfɪʃənt",
            "",
            [
                "making good, thorough, or careful use of resources; not consuming extra. Especially, making good use of time or energy",  # noqa
                "expressing the proportion of consumed energy that was successfully used in a process; the ratio of useful output to total input",  # noqa
                "causing effects, producing results; bringing into being; initiating change (rare except in philosophical and legal expression <i>efficient cause</i> = causative factor or agent)",  # noqa
                "<i>(proscribed, old use)</i> effective",
                "<i>(obsolete)</i> a cause; something that causes an effect",
            ],
        ),
        (
            "it's",
            "ɪts",
            "",
            [
                "It is.",
                "It has.",
                "<i>(colloquial)</i> There's, there is; there're, there are.",
                "<i>(now nonstandard)</i> <i>Alternative form of</i> <b>its</b>",
            ],
        ),
        (
            "on",
            "ɒn",
            "",
            [
                "In the state of being active, functioning or operating.",
                "Performing according to schedule; taking place.",
                "<i>(chiefly, UK, informal, usually negative)</i> Acceptable, appropriate.",
                "<i>(informal)</i> Destined, normally in the context of a challenge being accepted; involved, doomed.",
                "<i>(baseball, informal)</i> Having reached a base as a runner and being positioned there, awaiting further action from a subsequent batter.",  # noqa
                "<i>(euphemistic)</i> Menstruating.",
                "To an operating state.",
                "Along, forwards (continuing an action).",
                "In continuation, at length.",
                "<i>(cricket)</i> In, or towards the half of the field on the same side as the batsman's legs; the left side for a right-handed batsman; leg.",  # noqa
                "<i>(obsolete in the US)</i> Later.",
                "<i>Of betting odds, denoting a better than even chance.</i> <i>See also <b>odds-on</b></i>.",
                "Positioned at the upper surface of, touching from above.",
                "At or near; adjacent to.",
                "Covering.",
                "At the date of.",
                "Some time during the day of.",
                "Dealing with the subject of, about, or concerning something.",
                "Touching; hanging from.",
                "<i>(informal)</i> In the possession of.",
                "Because of, or due to.",
                "Upon; at the time of (and often because of).",
                "Paid for by.",
                "<i>Used to indicate a means or medium.</i>",
                "<i>Indicating a means of subsistence.</i>",
                "Away or occupied with (e.g. a scheduled activity).",
                "Denoting performance or action by contact with the surface, upper part, or outside of anything; hence, by means of; with.",  # noqa
                "Regularly taking (a drug).",
                "Under the influence of (a drug).",
                "<i>(mathematics)</i> Having identical domain and codomain.",
                "<i>(mathematics)</i> Having <math>V^n</math> as domain and <i>V</i> as codomain, for some set <i>V</i> and integer <i>n</i>.",  # noqa
                "<i>(mathematics)</i> Generated by.",
                "Supported by (the specified part of itself).",
                "At a given time after the start of something; at.",
                "In addition to; besides; indicating multiplication or succession in a series.",
                "<i>(obsolete, regional)</i> of",
                "Indicating dependence or reliance; with confidence in.",
                "Toward; for; indicating the object of an emotion.",
                "<i>(obsolete)</i> At the peril of, or for the safety of.",
                "In the service of; connected with; of the number of.",
                "By virtue of; with the pledge of.",
                "To the account or detriment of; denoting imprecation or invocation, or coming to, falling, or resting upon.",  # noqa
                "<i>(especially when numbers of combatants or competitors are specified)</i> Against; in opposition to.",  # noqa
                "<i>(transitive, Singapore, Philippines)</i> to switch on",
                "<i>(UK dialectal, Scotland)</i> Without.",
                "In the Japanese language, a pronunciation, or reading, of a kanji character that was originally based on the character's pronunciation in Chinese, contrasted with kun.",  # noqa
            ],
        ),
        (
            "portmanteau",
            "pɔːtˈmæn.təʊ",
            "",
            [
                "A large travelling case usually made of leather, and opening into two equal sections.",
                "<i>(Australia, dated)</i> A schoolbag.",
                "<i>(archaic)</i> A hook on which to hang clothing.",
                "<i>(attributive, linguistics)</i> Made by combining two (or more) words, stories, etc., in the manner of a linguistic portmanteau.",  # noqa
                "<i>(linguistics)</i> A portmanteau word.",
                "To make a portmanteau word.",
            ],
        ),
        (
            "someone",
            "ˈsʌmwʌn",
            "",
            [
                "Some person.",
                "A partially specified but unnamed person.",
                "an important person",
            ],
        ),
        (
            "the",
            "ˈðiː",
            "",
            [
                "<i>Definite grammatical article that implies necessarily that an entity it articulates is presupposed; something already mentioned, or completely specified later in that same sentence, or assumed already completely specified.</i> <small>[from 10th c.]</small>",  # noqa
                "<i>Used before a noun modified by a restrictive relative clause, indicating that the noun refers to a single referent defined by the relative clause.</i>",  # noqa
                "<i>Used before an object considered to be unique, or of which there is only one at a time.</i> <small>[from 10th c.]</small>",  # noqa
                "<i>Used before a superlative or an ordinal number modifying a noun, to indicate that the noun refers to a single item.</i>",  # noqa
                "<i>Added to a superlative or an ordinal number to make it into a substantive.</i> <small>[from 9th c.]</small>",  # noqa
                "<i>Introducing a singular term to be taken generically: preceding a name of something standing for a whole class.</i> <small>[from 9th c.]</small>",  # noqa
                "<i>Used before an adjective, indicating all things (especially persons) described by that adjective.</i> <small>[from 9th c.]</small>",  # noqa
                "<i>Used to indicate a certain example of (a noun) which is usually of most concern or most common or familiar.</i> <small>[from 12th c.]</small>",  # noqa
                "<i>Used before a body part (especially of someone previously mentioned), as an alternative to a possessive pronoun.</i> <small>[from 12th c.]</small>",  # noqa
                "<i>When stressed, indicates that it describes an object which is considered to be best or exclusively worthy of attention.</i> <small>[from 18th c.]</small>",  # noqa
                "<i>With a comparative or with <b>more</b> and a verb phrase, establishes a correlation with one or more other such comparatives.</i>",  # noqa
                "<i>With a comparative, and often with <b>for it</b>, indicates a result more like said comparative. This can be negated with <b>none</b>. See <b>none the</b>.</i>",  # noqa
                "For each; per.",
            ],
        ),
        (
            "um",
            "",
            "",
            [
                "<i>Expression of hesitation, uncertainty or space filler in conversation</i>. See uh.",
                "<i>(chiefly, US)</i> <i>(dated spelling of)</i>",
                "<i>(intransitive)</i> To make the <i>um</i> sound to express uncertainty or hesitancy.",
                "<i>Alternative form of</i> <b>umbe</b>",
                "<i>Alternative spelling of</i> <b>µm</b>",
                "<i>(dated, sometimes, humorous, often, offensive)</i> <i>An undifferentiated determiner or article; a miscellaneous linking word, or filler with nonspecific meaning; representation of broken English stereotypically or comically attributed to Native Americans.</i>",  # noqa
            ],
        ),
        (
            "us",
            "ʌs",
            "",
            [
                "<i>(personal)</i> Me and at least one other person; the objective case of <b>we</b>.",
                "<i>(colloquial)</i> Me.",
                "<i>(Northern England)</i> Our.",
                "The speakers/writers, or the speaker/writer and at least one other person.",
                "<i>Alternative spelling of</i> <b>µs</b>: microsecond",
            ],
        ),
        (
            "water",
            "ˈwɔːtə",
            "",
            [
                "<i>(uncountable)</i> A substance (of molecular formula H₂O) found at room temperature and pressure as a clear liquid; it is present naturally as rain, and found in rivers, lakes and seas; its solid form is ice and its gaseous form is steam.",  # noqa
                (
                    "<i>(uncountable, in particular)</i> The liquid form of this substance: liquid H₂O.",
                    "<i>(countable)</i> A serving of liquid water.",
                ),
                "<i>(alchemy, philosophy)</i> The aforementioned liquid, considered one of the Classical elements or basic elements of alchemy.",  # noqa
                "<i>(uncountable or in the plural)</i> Water in a body; an area of open water.",
                "<i>(poetic, archaic or dialectal)</i> A body of water, almost always a river.",
                "A combination of water and other substance(s).",
                (
                    "<i>(sometimes, countable)</i> Mineral water.",
                    "<i>(countable, often, in the plural)</i> Spa water.",
                    "<i>(pharmacy)</i> A solution in water of a gaseous or readily volatile substance.",
                    "Urine. <small>[from 15th c.]</small>",
                    'Amniotic fluid. (<i>Used only in the plural in the UK but often also in the singular in North America. (The Merriam-Webster Medical Dictionary says "often used in plural; also: bag of waters".)</i>)',  # noqa
                    "<i>(colloquial, medicine)</i> Fluids in the body, especially when causing swelling.",
                ),
                "<i>(figuratively, in the plural or in the singular)</i> A state of affairs; conditions; usually with an adjective indicating an adverse condition.",  # noqa
                "<i>(colloquial, figuratively)</i> A person's intuition.",
                "<i>(uncountable, dated, finance)</i> Excess valuation of securities.",
                "The limpidity and lustre of a precious stone, especially a diamond.",
                "A wavy, lustrous pattern or decoration such as is imparted to linen, silk, metals, etc.",
                "<i>(transitive)</i> To pour water into the soil surrounding (plants).",
                "<i>(transitive)</i> To wet or supply with water; to moisten; to overflow with water; to irrigate.",
                "<i>(transitive)</i> To provide (animals) with water for drinking.",
                "<i>(intransitive)</i> To get or take in water.",
                "<i>(transitive, colloquial)</i> To urinate onto.",
                "<i>(transitive)</i> To dilute.",
                "<i>(transitive, dated, finance)</i> To overvalue (securities), especially through deceptive accounting.",  # noqa
                "<i>(intransitive)</i> To fill with or secrete water.",
                "<i>(transitive)</i> To wet and calender, as cloth, so as to impart to it a lustrous appearance in wavy lines; to diversify with wavelike lines.",  # noqa
            ],
        ),
        (
            "word",
            "wɜːd",
            "",
            [
                "The smallest unit of language that has a particular meaning and can be expressed by itself; the smallest discrete, meaningful unit of language. (<i>contrast <i>morpheme</i>.</i>)",  # noqa
                (
                    "The smallest discrete unit of spoken language with a particular meaning, composed of one or more phonemes and one or more morphemes",  # noqa
                    "The smallest discrete unit of written language with a particular meaning, composed of one or more letters or symbols and one or more morphemes",  # noqa
                    "A discrete, meaningful unit of language approved by an authority or native speaker (<i>compare non-word</i>).",  # noqa
                ),
                "Something like such a unit of language:",
                (
                    "A sequence of letters, characters, or sounds, considered as a discrete entity, though it does not necessarily belong to a language or have a meaning",  # noqa
                    "<i>(telegraphy)</i> A unit of text equivalent to five characters and one space. <small>[from 19th c.]</small>",  # noqa
                    "<i>(computing)</i> A fixed-size group of bits handled as a unit by a machine and which can be stored in or retrieved from a typical register (so that it has the same size as such a register). <small>[from 20th c.]</small>",  # noqa
                    "<i>(computer science)</i> A finite string that is not a command or operator. <small>[from 20th or 21st c.]</small>",  # noqa
                    "<i>(group theory)</i> A group element, expressed as a product of group elements.",
                ),
                "The fact or act of speaking, as opposed to taking action. <small>[from 9th c]</small>.",
                "<i>(now, rare outside certain phrases)</i> Something that someone said; a comment, utterance; speech. <small>[from 10th c.]</small>",  # noqa
                "<i>(obsolete outside certain phrases)</i> A watchword or rallying cry, a verbal signal (even when consisting of multiple words).",  # noqa
                "<i>(obsolete)</i> A proverb or motto.",
                "News; tidings (<i>used without an article</i>). <small>[from 10th c.]</small>",
                "An order; a request or instruction; an expression of will. <small>[from 10th c.]</small>",
                "A promise; an oath or guarantee. <small>[from 10th c.]</small>",
                "A brief discussion or conversation. <small>[from 15th c.]</small>",
                "<i>(in the plural)</i> <i>See</i> <b>words</b>.",
                "<i>(theology, sometimes <b>Word</b>)</i> Communication from God; the message of the Christian gospel; the Bible, Scripture. <small>[from 10th c.]</small>",  # noqa
                "<i>(theology, sometimes <b>Word</b>)</i> Logos, Christ. <small>[from 8th c.]</small>",
                "<i>(transitive)</i> To say or write (something) using particular words; to phrase (something).",
                "<i>(transitive, obsolete)</i> To flatter with words, to cajole.",
                "<i>(transitive)</i> To ply or overpower with words.",
                "<i>(transitive, rare)</i> To conjure with a word.",
                "<i>(intransitive, archaic)</i> To speak, to use words; to converse, to discourse.",
                '<i>(slang, African-American Vernacular)</i> Truth, indeed, that is the truth! The shortened form of the statement "My word is my bond."',  # noqa
                "<i>(slang, emphatic, stereotypically, African-American Vernacular)</i> An abbreviated form of <b>word up</b>; a statement of the acknowledgment of fact with a hint of nonchalant approval.",  # noqa
                "<i>Alternative form of</i> <b>worth</b> (“to become”).",
            ],
        ),
    ],
)
def test_find_sections_and_definitions(word, pronunciation, genre, definitions, page):
    """Test the sections finder and definitions getter."""
    code = page(word, "en")
    details = parse_word(word, code, "en", force=True)
    assert pronunciation == details[0]
    assert genre == details[1]
    assert definitions == details[2]


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{abbreviation of|en|abortion}}", "<i>Abbreviation of</i> <b>abortion</b>"),
        ("{{alt form|enm|theen}}", "<i>Alternative form of</i> <b>theen</b>"),
        (
            "{{alt form|enm|a|pos=indefinite article}}",
            "<i>Alternative form of</i> <b>a</b> (indefinite article)",
        ),
        (
            "{{alt form|enm|worth|t=to become}}",
            "<i>Alternative form of</i> <b>worth</b> (“to become”)",
        ),
        (
            "{{alternative form of|enm|theen}}",
            "<i>Alternative form of</i> <b>theen</b>",
        ),
        (
            "{{alternative spelling of|en|µs}}",
            "<i>Alternative spelling of</i> <b>µs</b>",
        ),
        ("{{defdate|from 15th c.}}", "<small>[from 15th c.]</small>"),
        ("{{eye dialect of|en|is}}", "<i>Eye dialect spelling of</i> <b>is</b>"),
        ("{{gloss|liquid H<sub>2</sub>O}}", "(liquid H<sub>2</sub>O)"),
        ("{{IPAchar|[tʃ]|lang=en}}", "[tʃ]"),
        ("{{IPAfont|[[ʌ]]}}", "⟨ʌ⟩"),
        ("{{l|en|water vapour}}", "water vapour"),
        ("{{ll|en|cod}}", "cod"),
        ("{{link|en|water vapour}}", "water vapour"),
        ("{{m|en|more}}", "<b>more</b>"),
        ("{{n-g|Definite grammatical}}", "<i>Definite grammatical</i>",),
        (
            "{{non-gloss definition|Definite grammatical}}",
            "<i>Definite grammatical</i>",
        ),
        (
            "{{non-gloss definition|1=Definite grammatical}}",
            "<i>Definite grammatical</i>",
        ),
        (
            "{{qual|Used only in the plural in the UK}}",
            "(<i>Used only in the plural in the UK</i>)",
        ),
        (
            "{{qualifier|Used only in the plural in the UK}}",
            "(<i>Used only in the plural in the UK</i>)",
        ),
        (
            "{{taxlink|Gadus macrocephalus|species|ver=170710}}",
            "<i>Gadus macrocephalus</i>",
        ),
        ("{{vern|Pacific cod}}", "Pacific cod"),
    ],
)
def test_clean_template(wikicode, expected):
    """Test templates handling."""
    assert clean("foo", wikicode, "en") == expected
