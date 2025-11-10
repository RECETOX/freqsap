class Variation:
    def __init__(self, ref: str, position: int):
        self._id = ref
        self._position = position

    def valid(self) -> bool:
        # Placeholder implementation
        return self._id.startswith("rs") and self._position > 0

    def __str__(self) -> str:
        return self._id
