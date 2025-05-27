from service.state.occupancy_state import AvailableState, AlmostFullState, FullState


class OccupacyContext:
    def __init__(self, ticket_sold: int, room_capacity: int):
        self.ticket_sold = ticket_sold
        self.room_capacity = room_capacity
        self.state = self._determine_state()

    def _determine_state(self):
        occupacy_ratio = self.ticket_sold / self.room_capacity
        if occupacy_ratio >= 1.0:
            return FullState()
        elif occupacy_ratio >= 0.6:
            return AlmostFullState()
        else:
            return AvailableState()

    def get_state_label(self):
        return self.state.handle()
