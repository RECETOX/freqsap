from dataclasses import dataclass

from freqsap.allele import Allele


@dataclass
class Study:
    source: str
    population: str
    group: str
    size: int
    reference: Allele
    alternatives: list[Allele]
    bioproject: str
    biosample: str