from freqsap.accession import Accession
from freqsap.interfaces import ProteinVariantAPI
from freqsap.protein import Protein


class EBI(ProteinVariantAPI):
    def __init__(self):
        pass

    def available(self) -> bool:
        return False
    
    def get(self, accession: Accession) -> Protein:
        pass
