import json
import pytest
import requests
from freqsap.uniprot import UniProt


@pytest.fixture
def api() -> UniProt:
    return UniProt()


@pytest.fixture
def accession():
    return "P02788"


@pytest.fixture
def feature() -> dict:
    with open("tests/feature.json") as file:
        return json.load(file)


def test_available():
    sut = UniProt()
    expected = requests.get(url="https://google.com", timeout=1).ok
    assert sut.available() == expected


def test_query(api: UniProt, accession: str):
    sut = api.query(accession)
    assert sut["primaryAccession"] == accession
    assert len(sut["features"]) == 6


def test_is_dbsnp(api: UniProt):
    xref = {"database": "dbSNP", "id": "rs121913547"}

    assert api.is_dbsnp(xref) == True


def test_get(api: UniProt, accession: str):
    actual = api.get(accession)
    assert len(actual.variations) == 6
