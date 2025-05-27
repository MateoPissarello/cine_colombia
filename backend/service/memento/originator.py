from datetime import datetime
from models import MovieShowtime, days
from daos.MovieDAO import MovieDAO


class ShowtimeOriginator:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def create_memento(self, cinema_id: int):
        showtimes = self.dao.get_showtimes_by_cinema(cinema_id)
        state = [
            {
                "movie_id": s.movie_id,
                "cinema_room_id": s.cinema_room_id,
                "showtime": s.showtime.strftime("%H:%M"),
                "day_of_week": s.day_of_week.value,
            }
            for s in showtimes
        ]
        from .memento import ShowtimeMemento

        return ShowtimeMemento(state)

    def restore_from_memento(self, cinema_id: int, memento):
        self.dao.delete_all_showtimes_for_cinema(cinema_id)
        state = memento.get_state()

        for entry in state:
            showtime = MovieShowtime(
                movie_id=entry["movie_id"],
                cinema_room_id=entry["cinema_room_id"],
                showtime=datetime.strptime(entry["showtime"], "%H:%M").time(),
                day_of_week=days(entry["day_of_week"]),
            )
            self.dao.create_showtime(showtime)
