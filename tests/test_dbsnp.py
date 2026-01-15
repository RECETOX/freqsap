from freqsap.dbsnp import DBSNP


def test_init():
    sut = DBSNP()
    assert sut is not None

def test_get_is_not_none():
    sut = DBSNP()
    actual = sut.get("rs121913547")
    assert actual is not None