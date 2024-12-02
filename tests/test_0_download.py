import logging
import os
import re
from collections.abc import Callable
from pathlib import Path

import pytest
import responses

from wikidict import download
from wikidict.constants import BASE_URL, DUMP_URL

WIKTIONARY_INDEX = """<html>
<head><title>Index of /frwiktionary/</title></head>
<body bgcolor="white">
<h1>Index of /frwiktionary/</h1><hr><pre><a href="../">../</a>
<a href="20191120/">20191120/</a>                                          02-Jan-2020 01:29                   -
<a href="20191201/">20191201/</a>                                          21-Jan-2020 01:36                   -
<a href="20191220/">20191220/</a>                                          02-Feb-2020 01:28                   -
<a href="20200101/">20200101/</a>                                          21-Feb-2020 01:38                   -
<a href="20200120/">20200120/</a>                                          02-Mar-2020 01:28                   -
<a href="20200201/">20200201/</a>                                          02-Apr-2020 01:36                   -
<a href="20200220/">20200220/</a>                                          24-Feb-2020 17:32                   -
<a href="20200301/">20200301/</a>                                          09-Mar-2020 03:42                   -
<a href="20200514/">20200514/</a>                                          17-Apr-2020 15:20                   -
<a href="latest/">latest/</a>                                              17-Apr-2020 15:20                   -
</pre><hr></body>
</html>
"""
DUMPS = sorted(re.findall(r'href="(\d+)/"', WIKTIONARY_INDEX))


def cleanup(folder: Path) -> None:
    for file in folder.glob("pages-*.xml"):
        file.unlink()
    for file in folder.glob("pages-*.xml.bz2"):
        file.unlink()


@responses.activate
def test_simple(craft_data: Callable[[str], bytes]) -> None:
    """It should download the Wiktionary dump file and extract it."""

    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    date = DUMPS[-1]
    pages_xml = output_dir / f"pages-{date}.xml"
    pages_bz2 = output_dir / f"pages-{date}.xml.bz2"

    # Clean-up before we start
    cleanup(output_dir)

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(responses.GET, BASE_URL.format("fr"), body=WIKTIONARY_INDEX)
    responses.add(responses.GET, DUMP_URL.format("fr", date), body=craft_data("fr"))

    # Start the whole process
    assert download.main("fr") == 0

    # Check that files are created
    assert pages_xml.is_file()
    assert pages_bz2.is_file()


@responses.activate
def test_download_already_done(craft_data: Callable[[str], bytes]) -> None:
    """It should not download again a processed Wiktionary dump."""

    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    date = DUMPS[-1]
    pages_xml = output_dir / f"pages-{date}.xml"
    pages_bz2 = output_dir / f"pages-{date}.xml.bz2"

    # The BZ2 file was already downloaded
    pages_bz2.write_bytes(craft_data("fr"))

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    responses.add(responses.GET, BASE_URL.format("fr"), body=WIKTIONARY_INDEX)

    # Start the whole process
    assert download.main("fr") == 0

    # Check that files are created
    assert pages_xml.is_file()
    assert pages_bz2.is_file()


@responses.activate
def test_ongoing_dump(craft_data: Callable[[str], bytes]) -> None:
    """When a dump is not finished on the Wiktionary side, the previous dump should be used until a valid one is found."""

    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    expected_dump = DUMPS[-3]
    assert expected_dump == "20200220"

    # Clean-up before we start
    cleanup(output_dir)

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages() for 20200514, 20200301, and 20200220
    responses.add(responses.GET, BASE_URL.format("fr"), body=WIKTIONARY_INDEX)
    for dump in DUMPS[:-3:-1]:
        responses.add(responses.GET, DUMP_URL.format("fr", dump), status=404)
    responses.add(responses.GET, DUMP_URL.format("fr", expected_dump), body=craft_data("fr"))

    # Start the whole process
    assert download.main("fr") == 0

    # Check that files are created
    assert (output_dir / f"pages-{expected_dump}.xml").is_file()
    assert (output_dir / f"pages-{expected_dump}.xml.bz2").is_file()

    # Check that files are not created
    assert not (output_dir / "pages-20200514.xml").is_file()
    assert not (output_dir / "pages-20200514.xml.bz2").is_file()
    assert not (output_dir / "pages-20200301.xml").is_file()
    assert not (output_dir / "pages-20200301.xml.bz2").is_file()


@responses.activate
def test_no_dump_found(craft_data: Callable[[str], bytes]) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    # Clean-up before we start
    cleanup(output_dir)

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages() for all dumps
    responses.add(responses.GET, BASE_URL.format("fr"), body=WIKTIONARY_INDEX)
    for dump in DUMPS:
        responses.add(responses.GET, DUMP_URL.format("fr", dump), status=404)

    # Start the whole process
    assert download.main("fr") == 1

    # Check that files are created
    for dump in DUMPS:
        assert not (output_dir / f"pages-{dump}.xml").is_file()
        assert not (output_dir / f"pages-{dump}.xml.bz2").is_file()


def test_progress_callback(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.DEBUG):
        download.callback_progress("Some text", 42 * 1024, False)
        download.callback_progress("Some text", 42 * 1024, True)

    assert caplog.records[0].getMessage() == "Some text: 43,008 bytes"
    assert caplog.records[1].getMessage() == "Some text: OK [43,008 bytes]"
