from sqlalchemy.orm import Session
from daos.MaintenanceRequestDAO import MaintenaceRequestDAO
from daos.MovieDAO import MovieDAO
from daos.CinemaDAO import CinemaDAO
from models import Movie, MovieShowtime
from typing import List
from service.memento.originator import ShowtimeOriginator
from service.memento.caretaker import SnapshotCaretaker
from daos.ShowtimeSnapshotDAO import ShowtimeSnapshotDAO
from utils.iterators.movie_showtime_iterator import MovieShowtimeCollection


class MovieService:
    def __init__(self, db: Session):
        self.db = db
        self.request_dao = MaintenaceRequestDAO(db)
        self.movie_dao = MovieDAO(db)
        self.cinema_dao = CinemaDAO(db)

    def save_programming_snapshot(self, cinema_id: int) -> None:
        """
        Save a snapshot of the current movie programming for a specific cinema.
        """
        try:
            cinema = self.cinema_dao.get_cinema(cinema_id)
            if not cinema:
                raise ValueError("Cinema not found")
            snapshot_dao = ShowtimeSnapshotDAO(self.db)
            originator = ShowtimeOriginator(self.movie_dao)
            caretaker = SnapshotCaretaker(snapshot_dao)

            memento = originator.create_memento(cinema_id)
            caretaker.store_snapshot(cinema_id, memento)
        except Exception as e:
            raise ValueError(f"Error saving programming snapshot: {str(e)}")

    def restore_last_snapshot(self, cinema_id: int) -> None:
        """
        Restore the last snapshot of movie programming for a specific cinema.
        """
        try:
            cinema = self.cinema_dao.get_cinema(cinema_id)
            if not cinema:
                raise ValueError("Cinema not found")
            snapshot_dao = ShowtimeSnapshotDAO(self.db)
            originator = ShowtimeOriginator(self.movie_dao)
            caretaker = SnapshotCaretaker(snapshot_dao)

            memento = caretaker.retrieve_latest_snapshot(cinema_id)
            if not memento:
                raise ValueError("No snapshots found for this cinema")

            originator.restore_from_memento(cinema_id, memento)
        except Exception as e:
            raise ValueError(f"Error restoring snapshot: {str(e)}")

    def create_movie(self, movie_data: Movie) -> Movie:
        """
        Create a new movie.
        """
        try:
            movie = self.movie_dao.create_movie(movie_data)
            return movie
        except Exception as e:
            raise ValueError(f"Error creating movie: {str(e)}")

    def get_movies(self) -> List[Movie]:
        """
        Get all movies.
        """
        try:
            movies = self.movie_dao.get_movies()
            return movies
        except Exception as e:
            raise ValueError(f"Error retrieving movies: {str(e)}")

    def get_showtimes_iterator_for_cinema(self, cinema_id: int) -> MovieShowtimeCollection:
        """
        Get an iterator for movie showtimes for a specific cinema.
        """
        try:
            cinema = self.cinema_dao.get_cinema(cinema_id)
            if not cinema:
                raise ValueError("Cinema not found")

            showtimes = self.movie_dao.get_showtimes_by_cinema(cinema_id)
            return MovieShowtimeCollection(showtimes)
        except Exception as e:
            raise ValueError(f"Error retrieving showtimes: {str(e)}")

    def create_showtime(self, request_data: MovieShowtime) -> MovieShowtime:
        """
        Create a new movie showtime.
        """
        try:
            # Validate the cinema room exists
            cinema_room = self.cinema_dao.get_cinema_room(request_data.cinema_room_id)
            if not cinema_room:
                raise ValueError("Cinema room not found")
            movie = self.movie_dao.get_movie_by_id(request_data.movie_id)
            if not movie:
                raise ValueError("Movie not found")
            if not self.movie_dao.is_showtime_available(
                request_data.cinema_room_id,
                request_data.day_of_week,
                request_data.showtime,
                movie.duration,
            ):
                raise ValueError("Showtime is not available for the specified cinema room and day")
            # Create the showtime
            showtime = self.movie_dao.create_showtime(request_data)
            return showtime
        except Exception as e:
            raise ValueError(f"Error creating showtime: {str(e)}")
