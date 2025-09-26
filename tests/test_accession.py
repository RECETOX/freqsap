import pytest
from freqsap.accession import Accession


def test_init():
    sut = Accession("")
    assert sut is not None


@pytest.mark.parametrize("accession, expected", [["test", False], ["P02788", True], ["PAB", False]])
def test_valid(accession, expected):
    sut = Accession(accession)  # arrange
    actual = sut.valid()  # act
    assert actual == expected  # assert


def test_to_string():
    sut = Accession("P02788")
    assert str(sut) == "P02788"
