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

    def header(self) -> list[str]:
        return self.row().keys()
    
    def row(self) -> dict:
        base = {
            'study': self.source,
            'population': self.population,
            'group': self.group,
            'size': self.size,
            'ref_allele_na': self.reference.nucleotide,
            'ref_allele_freq': self.reference.frequency
        }

        for i in range(len(self.alternatives)):
            alternative = self.alternatives[i]
            base.update({
                f'alt_allele_{i+1}_na': alternative.nucleotide,
                f'alt_allele_{i+1}_freq': alternative.frequency
            })
        
        return base

