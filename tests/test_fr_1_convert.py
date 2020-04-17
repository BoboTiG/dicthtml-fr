import os
from pathlib import Path
from zipfile import ZipFile

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
from scripts import constants as C  # noqa
from scripts import convert  # noqa


def test_main(data):
    """Test the JSON -> HTML conversion."""
    # Start the whole process
    assert convert.main() == 0

    # Check for the final ZIP file
    dicthtml = C.SNAPSHOT / f"dicthtml-fr.zip"
    assert dicthtml.is_file()

    # Check the ZIP content
    with ZipFile(dicthtml) as fh:
        expected = [
            "qu.html",
            "sl.html",
            "ac.html",
            "au.html",
            "ba.html",
            "em.html",
            "ic.html",
            "l’.html",
            "mo.html",
            "pi.html",
            "œc.html",
            "words",
            "words.count",
            "words.snapshot",
        ]
        assert fh.namelist() == expected
