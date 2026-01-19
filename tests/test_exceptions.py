from freqsap.exceptions import AccessionNotFoundError


def test_can_create():
    actual = AccessionNotFoundError("")
    assert actual is not None
