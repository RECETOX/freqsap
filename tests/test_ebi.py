from freqsap.ebi import EBI
from freqsap.interfaces import ProteinVariantAPI


def test_can_create():
    actual = EBI()
    assert actual is not None

def test_is_api():
    assert issubclass(EBI, ProteinVariantAPI)