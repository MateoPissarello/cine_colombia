class ShowtimeMemento:
    def __init__(self, state: list[dict]):
        self._state = state

    def get_state(self) -> list[dict]:
        return self._state
