class Variation:
    def __init__(self, id: str):
        self._id = id

    def valid(self) -> bool:
        # Placeholder implementation
        return self._id.startswith("rs")

    def __str__(self) -> str:
        return self._id
