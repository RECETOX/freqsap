from dataclasses import dataclass


@dataclass
class Variation:
    ref: str
    position: int

    def valid(self) -> bool:
        # Placeholder implementation
        return self.ref.startswith("rs") and self.position > 0

    def __str__(self) -> str:
        return self.ref
