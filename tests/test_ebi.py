import pytest
import requests
from freqsap.accession import Accession
from freqsap.ebi import EBI
from freqsap.exceptions import AccessionNotFound
from freqsap.interfaces import ProteinVariantAPI


def ebi_is_available() -> bool:
    r = requests.get(
        "https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100", headers={"Accept": "application/json"},
    )
    responseBody = r.text
    expected_response = '{"requestedURL":"https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100","errorMessage":["At least one of these request parameters is required: accession, disease, omim, evidence, taxid, dbtype or dbid"]}'
    return responseBody == expected_response


@pytest.fixture
def api() -> EBI:
    return EBI()


@pytest.fixture
def accession() -> str:
    return "P02788"


def test_can_create():
    actual = EBI()
    assert actual is not None


def test_is_api():
    assert issubclass(EBI, ProteinVariantAPI)


def test_is_available():
    expected = ebi_is_available()
    actual = EBI().available()
    assert actual == expected


def test_get(api: EBI, accession: str):
    actual = api.get(accession)
    assert actual is not None


def test_get_non_existing_accession(api: EBI):
    non_existing_accession = Accession("P54321")
    with pytest.raises(AccessionNotFound) as e:
        EBI().get(non_existing_accession)
        assert e.message == "Accession P54321 not found."


def test_has_all_variants(api: EBI):
    variants = api.get("P02792").variations
    refs = [var.ref for var in variants]
    assert all(refs)
    assert len(variants) >= 200
