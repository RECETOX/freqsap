# ruff: noqa: PLR2004
import pytest
import requests
from freqsap.uniprot import UniProt
from tests import internet


@pytest.fixture
def api() -> UniProt:
    """Fixture to create UniProt API endpoint."""
    return UniProt()


@pytest.fixture(params=["P02788", "P02792", "P0DJI9"])
def accession(request):
    """Fixture to get valid protein accession as a string."""
    return request.param


@pytest.mark.skipif(not internet(), reason="Can't connect to network!")
def test_available():
    """Test if UniProt endpoint is available."""
    sut = UniProt()
    expected = requests.get(url="https://google.com", timeout=3).ok
    assert sut.available() == expected


@pytest.mark.skipif(not internet(), reason="Can't connect to network!")
def test_query(api: UniProt, accession: str):
    """Test whether query function returns expected result."""
    sut = api.query(accession)
    assert sut["primaryAccession"] == accession


def test_is_dbsnp(api: UniProt):
    """Check whetehr an xref points to dbsnp."""
    xref = {"database": "dbSNP", "id": "rs121913547"}
    assert api.is_dbsnp(xref)


@pytest.mark.skipif(not internet(), reason="Can't connect to network!")
def test_get(api: UniProt, accession: str):
    """Test whether we can get the protein specified by the accession and it has all variations."""
    actual = api.get(accession)
    assert actual.variations is not None


def test_has_all_variants(api: UniProt):
    """Second test whether specified protein has all variations."""
    variants = api.get("P02792").variations
    assert len(variants) == 2


@pytest.mark.skipif(not internet(), reason="Can't connect to network!")
def test_get_is_reproducible(api: UniProt, accession: str):
    """Test whether repeated requests for the same accession return the same variants."""
    first = api.get(accession).variations
    second = api.get(accession).variations
    assert [repr(v) for v in first] == [repr(v) for v in second]
