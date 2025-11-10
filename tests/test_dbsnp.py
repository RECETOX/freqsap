from freqsap.dbsnp import DBSNP


def test_init():
    sut = DBSNP()
    assert sut is not None