class Variation:
    def __init__(self, ref: str):
        self._id = ref

    def valid(self) -> bool:
        # Placeholder implementation
        return self._id.startswith("rs")

    def __str__(self) -> str:
        return self._id
