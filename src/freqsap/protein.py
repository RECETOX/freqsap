from typing import Iterable

from freqsap.accession import Accession
from freqsap.variation import Variation


class Protein:
    def __init__(self, accession: Accession, variations: Iterable[Variation]):
        self._accession = accession
        self._variations = variations

    @property
    def variations(self) -> Iterable[Variation]:
        """Get the variations associated with this protein."""
        return self._variations
