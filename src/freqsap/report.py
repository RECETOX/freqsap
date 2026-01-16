from freqsap.study import Study
from freqsap.variation import Variation

class ReferenceSNPReport:
    def __init__(self, variation: Variation, metadata: dict, studies: list[Study]):
        self._variation: Variation = variation
        self._metadata: dict = metadata
        self._studies: list[Study] = studies
    
    def header(self) -> list[str]:
        fields = ['id', 'position']
        for study in self._studies:
            for entry in study.header():
                if not (entry in fields):
                    fields.append(entry)       
        return fields
    
    def rows(self) -> list[dict]:
        _base = {'id': self._variation.ref, 'position': self._variation.position}
        return [_base | study.row() for study in self._studies]
