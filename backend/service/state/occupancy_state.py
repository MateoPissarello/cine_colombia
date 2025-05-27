from abc import ABC, abstractmethod


class OccupancyState(ABC):
    @abstractmethod
    def handle(self):
        pass

    @abstractmethod
    def name(self):
        pass


class AvailableState(OccupancyState):
    def handle(self):
        return "The cinema is available for bookings."

    def name(self):
        return "Available"


class AlmostFullState(OccupancyState):
    def handle(self):
        return "The cinema is almost full, hurry up to book your tickets!"

    def name(self):
        return "Almost Full"


class FullState(OccupancyState):
    def handle(self):
        return "The cinema is fully booked, no more tickets available."

    def name(self):
        return "Full"
