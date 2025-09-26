from abc import ABC, abstractmethod

from freqsap.accession import Accession
from freqsap.frequencies import Frequencies
from freqsap.protein import Protein
from freqsap.variation import Variation

# Interface for protein variant data sources
class ProteinVariantAPI(ABC):
    @abstractmethod
    def get(self, accession: Accession) -> Protein:
        pass

    @abstractmethod
    def available(self) -> bool:
        pass

# Interface for variant frequency data sources
class VariantFrequencyAPI(ABC):
    @abstractmethod
    def get(self, variation: Variation) -> Frequencies:
        pass

    @abstractmethod
    def available(self) -> bool:
        pass
