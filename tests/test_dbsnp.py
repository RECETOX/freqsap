import pytest
from freqsap.dbsnp import DBSNP
from freqsap.variation import Variation


@pytest.fixture
def variation() -> Variation:
    """Fixture to generate a variation."""
    return Variation("rs768011218", 1)

@pytest.fixture
def api() -> DBSNP:
    return DBSNP(timeout = 30)


def test_init():
    """Test if API service can be initiated."""
    sut = DBSNP()
    assert sut is not None


def test_get_is_not_none(api: DBSNP, variation: Variation):
    """Test whether interface implementation is not None."""
    actual = api.get(variation)
    assert actual is not None


def test_header(api: DBSNP, variation: Variation):
    """Test whether the header of the ReferenceSNPReport is valid."""
    actual = api.get(variation).header()
    assert actual == [
        "id",
        "position",
        "study",
        "population",
        "group",
        "size",
        "ref_allele_na",
        "ref_allele_freq",
        "alt_allele_1_na",
        "alt_allele_1_freq",
        "alt_allele_2_na",
        "alt_allele_2_freq",
    ]


def test_weird_variation_is_none(api: DBSNP):
    """Test different variation whether it is None, as it shouldn't retrieve a Report."""
    report = api.get("rs1250527354")
    assert report is None
