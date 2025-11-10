from freqsap.frequencies import Frequencies
from freqsap.interfaces import VariantFrequencyAPI
from freqsap.variation import Variation


class DBSNP(VariantFrequencyAPI):
    def get(self, variation: Variation) -> Frequencies:
        # Placeholder implementation
        pass

    def available(self) -> bool:
        # Placeholder implementation
        return True
