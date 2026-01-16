from freqsap.exceptions import AccessionNotFound


def test_can_create():
    actual = AccessionNotFound("")
    assert actual is not None
