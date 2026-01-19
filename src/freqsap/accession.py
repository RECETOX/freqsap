import re


class Accession:
    """Protein accession."""
    def __init__(self, accession: str):
        self._id = accession
        self._pattern = r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"

    def valid(self) -> bool:
        """Validate the accession using the built in regex pattern.

        Returns:
            bool: True if valid, otherwise False.
        """
        return re.fullmatch(self._pattern, self._id) is not None

    def __str__(self) -> str:
        return self._id
