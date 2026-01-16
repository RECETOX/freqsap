import pytest
from freqsap.allele import Allele
from freqsap.study import Study


@pytest.fixture
def study() -> Study:
    return Study("a study", "inhabitants of brno", "random", 10, Allele("T", 0.9), [Allele("C", 0.1)])


def test_header(study: Study):
    actual = study.header()
    expected = {
            "study",
            "population",
            "group",
            "size",
            "ref_allele_na",
            "ref_allele_freq",
            "alt_allele_1_na",
            "alt_allele_1_freq",
        }
    assert actual == expected
