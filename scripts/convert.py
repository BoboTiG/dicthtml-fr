"""Convert words from JSON data to eBook format (ZIP)."""
import gzip
import json
import sys
from collections import defaultdict
from contextlib import suppress
from pathlib import Path
from shutil import rmtree
from typing import List
from zipfile import ZIP_DEFLATED, ZipFile

from marisa_trie import Trie

from . import constants as C
from . import types as T


def craft_index(wordlist: List[str]) -> Path:
    """Generate the special file "words" that is an index of all words."""
    output = C.WORKING_DIR / "words"
    trie = Trie(wordlist)
    trie.save(output)
    return output


def make_groups(words: T.Words) -> T.Groups:
    """Group word by "index" ({letter1}{letter2}) for later HTML creation,
    see save().
    """
    groups: T.Groups = defaultdict(dict)

    for word, data in words.items():
        char_1, char_2 = word[0].lower(), word[1].lower()
        group = "11" if char_1 < "a" or char_2 < "a" else word[:2].lower()
        groups[group][word] = data

    return groups


def load() -> T.Words:
    """Load the big JSON file containing all words and their details."""
    with C.SNAPSHOT_DATA.open(encoding="utf-8") as fh:
        words: T.Words = json.load(fh)
    print(f">>> Loaded {len(words):,} words from {C.SNAPSHOT_DATA}")
    return words


def save(groups: T.Groups) -> None:
    """
    Format of resulting dicthtml-LOCALE.zip:

        aa.html
        ab.html
        ..
        words

    Each word must be stored into the file {letter1}{letter2}.html (gzip content).
    """

    # Files to add to the final archive
    to_compress = []

    # First, create individual HTML files
    wordlist: List[str] = []
    print(">>> Generating HTML files ", end="", flush=True)
    for count, (group, words) in enumerate(groups.items(), start=1):
        to_compress.append(save_html(group, words))
        wordlist.extend(words.keys())
        print(".", end="", flush=True)
    print()

    # Then create the special "words" file
    to_compress.append(craft_index(sorted(wordlist)))

    # Add unrealted files, just for history
    to_compress.append(C.SNAPSHOT_COUNT)
    to_compress.append(C.SNAPSHOT_FILE)

    # Finally, create the ZIP
    with ZipFile(C.DICTHTML, mode="w", compression=ZIP_DEFLATED) as fh:
        for file in to_compress:
            fh.write(file, arcname=file.name)

    print(f">>> Generated {C.DICTHTML} ({C.DICTHTML.stat().st_size:,} bytes)")


def save_html(name: str, words: T.Words) -> Path:
    """Generate individual HTML files.

    Content of the HTML file:

        <?xml version="1.0" encoding="utf-8"?>
        <html>
            word 1
            word 2
            ...
        </html>

    Syntax of each WORD:

        <w>
            <p>
                <a name="word"/>
                <b>word</b> [pronunciation] <i>genre</i>
                <br/>
                <br/>
                <ol>
                    <li>definition 1</li>
                    <li>definition 2</li>
                </ol>
            </p>
        </w>
    """

    # Word format
    fmt = (
        '<w><p><a name="{word}"/><b>{word}</b>{pronunciation}{genre}'
        "<br/><br/><ol>{definitions}</ol></p></w>"
    )

    # Save to uncompressed HTML
    raw_output = C.WORKING_DIR / f"{name}.raw.html"
    with raw_output.open(mode="w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>')

        for word, (_, pronunciation, genre, defs) in words.items():
            definitions = "".join(f"<li>{d}</li>" for d in defs)
            if pronunciation:
                pronunciation = f" \\{pronunciation}\\"
            if genre:
                genre = f" <i>{genre}.</i>"

            fh.write(
                fmt.format(
                    word=word,
                    pronunciation=pronunciation,
                    genre=genre,
                    definitions=definitions,
                )
            )

        fh.write("</html>\n")

    # Compress the HTML with gzip
    output = C.WORKING_DIR / f"{name}.html"
    with raw_output.open(mode="rb") as fi, gzip.open(output, mode="wb") as fo:
        fo.writelines(fi)

    return output


def main() -> int:
    """Extry point."""

    # Clean-up before starting
    with suppress(FileNotFoundError):
        rmtree(C.WORKING_DIR)
    C.WORKING_DIR.mkdir()

    # Retrieve all words
    words = load()

    # Create groups of words
    groups = make_groups(words)

    # Save to HTML pages and the fial ZIP
    save(groups)

    print(">>> Conversion done!")
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
