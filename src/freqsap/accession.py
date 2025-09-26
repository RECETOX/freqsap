import re


class Accession():
    def __init__(self, id: str):
        self._id = id
        self._pattern = r'[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}'
    
    def valid(self) -> bool:
        return re.fullmatch(self._pattern, self._id) is not None