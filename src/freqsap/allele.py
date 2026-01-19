from dataclasses import dataclass


@dataclass
class Allele:
    """Class to represent an allele."""
    nucleotide: str
    frequency: float
