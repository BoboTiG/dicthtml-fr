import os
from pathlib import Path
from zipfile import ZipFile

from scripts.convert import main


def test_main():
    """Test the JSON -> HTML conversion."""

    # Start the whole process
    assert main("fr") == 0

    # Check for the final ZIP file
    dicthtml = Path(os.environ["CWD"]) / "data" / "fr" / "dicthtml-fr.zip"
    assert dicthtml.is_file()

    # Check the ZIP content
    with ZipFile(dicthtml) as fh:
        expected = [
            "11.html",
            "INSTALL.txt",
            "aa.html",
            "ac.html",
            "au.html",
            "ba.html",
            "co.html",
            "de.html",
            "du.html",
            "ef.html",
            "em.html",
            "en.html",
            "ge.html",
            "gr.html",
            "gè.html",
            "ic.html",
            "ko.html",
            "mi.html",
            "mo.html",
            "mu.html",
            "na.html",
            "pi.html",
            "pr.html",
            "ra.html",
            "sa.html",
            "si.html",
            "sl.html",
            "words",
            "words.count",
            "words.snapshot",
            "ép.html",
            "œc.html",
            "πa.html",
        ]
        assert sorted(fh.namelist()) == expected

        # testfile returns the name of the first corrupt file, or None
        errors = fh.testzip()
        assert errors is None
