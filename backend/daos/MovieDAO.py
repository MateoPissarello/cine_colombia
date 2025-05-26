from sqlalchemy.orm import Session
from models import Movie, MovieShowtime, CinemaRoom
from typing import List
from datetime import datetime, timedelta, time


class MovieDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_movie(self, request_data: Movie) -> Movie:
        self.db.add(request_data)
        self.db.commit()
        self.db.refresh(request_data)
        return request_data

    def is_showtime_available(self, cinema_room_id: int, day_of_week: str, new_start: time, new_duration: int) -> bool:
        new_start_dt = datetime.combine(datetime.today(), new_start)
        new_end_dt = new_start_dt + timedelta(minutes=new_duration)

        existing_showtimes = (
            self.db.query(MovieShowtime)
            .filter(MovieShowtime.cinema_room_id == cinema_room_id, MovieShowtime.day_of_week == day_of_week)
            .all()
        )

        for showtime in existing_showtimes:
            existing_start_dt = datetime.combine(datetime.today(), showtime.showtime)
            temp_movie = self.db.query(Movie).filter(Movie.id == showtime.movie_id).first()
            existing_end_dt = existing_start_dt + timedelta(minutes=temp_movie.duration)

            if new_start_dt < existing_end_dt and existing_start_dt < new_end_dt:
                # Hay solapamiento
                return False

        return True

    def get_movies_for_cinema(self, cinema_id: int) -> List[Movie]:
        movies = (
            self.db.query(Movie)
            .join(MovieShowtime, Movie.id == MovieShowtime.movie_id)
            .filter(MovieShowtime.cinema_room_id == cinema_id)
            .all()
        )
        return movies

    def get_movies(self) -> List[Movie]:
        movies = self.db.query(Movie).all()
        return movies

    def get_movie_by_id(self, movie_id: int) -> Movie | None:
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        return movie

    def create_showtime(self, request_data: MovieShowtime) -> MovieShowtime:
        self.db.add(request_data)
        self.db.commit()
        self.db.refresh(request_data)
        return request_data

    def get_showtimes_by_cinema(self, cinema_id: int) -> List[MovieShowtime]:
        showtimes = (
            self.db.query(MovieShowtime)
            .join(CinemaRoom, MovieShowtime.cinema_room_id == CinemaRoom.id)
            .filter(CinemaRoom.cinema_id == cinema_id)
            .all()
        )
        return showtimes


def delete_showtime(self, showtime_id: int) -> bool:
    showtime = self.db.query(MovieShowtime).filter(MovieShowtime.id == showtime_id).first()
    if showtime:
        self.db.delete(showtime)
        self.db.commit()
        return True
    return False
