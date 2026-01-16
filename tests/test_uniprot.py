import json
from pathlib import Path
import pytest
import requests
from freqsap.uniprot import UniProt
from tests import internet


@pytest.fixture
def api() -> UniProt:
    return UniProt()


@pytest.fixture
def accession():
    return "P02788"


@pytest.fixture
def feature() -> dict:
    with Path.open("tests/feature.json") as file:
        return json.load(file)


@pytest.mark.skipif(internet() == False, reason="Can't connect to network!")
def test_available():
    sut = UniProt()
    expected = requests.get(url="https://google.com", timeout=1).ok
    assert sut.available() == expected


@pytest.mark.skipif(internet() == False, reason="Can't connect to network!")
def test_query(api: UniProt, accession: str):
    sut = api.query(accession)
    expected = 6
    assert sut["primaryAccession"] == accession
    assert len(sut["features"]) == expected


def test_is_dbsnp(api: UniProt):
    xref = {"database": "dbSNP", "id": "rs121913547"}

    assert api.is_dbsnp(xref)


@pytest.mark.skipif(internet() == False, reason="Can't connect to network!")
def test_get(api: UniProt, accession: str):
    actual = api.get(accession)
    expected = 6
    assert len(actual.variations) == expected

def test_has_all_variants(api: UniProt):
    variants = api.get('P02792').variations
    assert len(variants) == 2