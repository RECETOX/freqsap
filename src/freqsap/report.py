from freqsap.study import Study

class ReferenceSNPReport:
    def __init__(self, metadata: dict, studies: list[Study]):
        self._metadata = metadata
        self._studies = studies
