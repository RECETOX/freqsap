import pytest
from freqsap.variation import Variation


def test_init():
    sut = Variation("")
    assert sut is not None


@pytest.mark.parametrize("ref, expected",
    [
        ("test", False),
        ("rs1234", True),
    ],
)
def test_valid(ref: str, expected: bool):
    sut = Variation(ref)  # arrange
    actual = sut.valid()  # act
    assert actual == expected  # assert


def test_to_string():
    sut = Variation("rs1234")
    assert str(sut) == "rs1234"
