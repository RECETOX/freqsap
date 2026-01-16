import pytest
from freqsap.dbsnp import DBSNP
from freqsap.variation import Variation


@pytest.fixture
def variation() -> Variation:
    return Variation("rs768011218", 1)

def test_init():
    sut = DBSNP()
    assert sut is not None

def test_get_is_not_none(variation: Variation):
    sut = DBSNP()
    actual = sut.get(variation)
    assert actual is not None

def test_header(variation: Variation):
    actual = DBSNP().get(variation).header()
    assert actual == ['id', 'position', 'study', 'population', 'group', 'size', 'ref_allele_na', 'ref_allele_freq', 'alt_allele_1_na', 'alt_allele_1_freq', 'alt_allele_2_na', 'alt_allele_2_freq']

def test_weird_variation_is_none():
    sut = DBSNP()
    report = sut.get('rs1250527354')
    assert report is None