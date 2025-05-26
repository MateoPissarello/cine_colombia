from models import MovieShowtime
from typing import List


class MovieShowtimeIterator:
    def __init__(self, movie_showtimes: List[MovieShowtime]):
        self._movie_showtimes = movie_showtimes
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._movie_showtimes):
            result = self._movie_showtimes[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def reset(self):
        """Reset the iterator to the beginning."""
        self._index = 0
        return self


class MovieShowtimeCollection:
    def __init__(self, movie_showtimes: List[MovieShowtime]):
        self._movie_showtimes = movie_showtimes

    def __iter__(self):
        return MovieShowtimeIterator(self._movie_showtimes)

    def filter_by_day(self, day_of_week: str):
        """Filter movie showtimes by day of the week."""
        filtered_showtimes = [showtime for showtime in self._movie_showtimes if showtime.day_of_week == day_of_week]
        return MovieShowtimeIterator(filtered_showtimes)

    def filter_by_room(self, cinema_room_id: int):
        """Filter movie showtimes by cinema room ID."""
        filtered_showtimes = [
            showtime for showtime in self._movie_showtimes if showtime.cinema_room_id == cinema_room_id
        ]
        return MovieShowtimeIterator(filtered_showtimes)
