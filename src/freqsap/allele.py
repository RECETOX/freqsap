from dataclasses import dataclass


@dataclass
class Allele:
    nucleotide: str
    frequency: float
