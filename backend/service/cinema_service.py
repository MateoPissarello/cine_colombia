from sqlalchemy.orm import Session
from daos.CinemaDAO import CinemaDAO
from models import Cinema, CinemaRoom


class CinemaService:
    def __init__(self, db: Session):
        self.db = db
        self.cinema_dao = CinemaDAO(db)

    def create_cinema(self, cinema: Cinema) -> Cinema:
        """
        Create a new cinema.
        """
        try:
            data = self.cinema_dao.create_cinema(cinema)
            return data
        except Exception as e:
            raise ValueError(f"Error creating cinema: {str(e)}")

    def create_cinema_room(self, cinema_room: CinemaRoom) -> CinemaRoom:
        """
        Create a new cinema room.
        """
        try:
            if not self.cinema_dao.get_cinema(cinema_room.cinema_id):
                raise ValueError("Cinema does not exist")

            if self.cinema_dao.get_cinema_room_by_number(cinema_room.cinema_id, cinema_room.room_number):
                raise ValueError("Cinema room with this number already exists in the cinema")

            data = self.cinema_dao.create_cinema_room(cinema_room)
            return data
        except Exception as e:
            raise ValueError(f"Error creating cinema room: {str(e)}")

    def get_cinema_rooms_by_cinema_id(self, cinema_id: int) -> list[CinemaRoom]:
        """
        Get all cinema rooms by cinema ID.
        """
        try:
            if not self.cinema_dao.get_cinema(cinema_id):
                raise ValueError("Cinema with this ID does not exist")
            return self.cinema_dao.get_rooms_by_cinema_id(cinema_id)
        except Exception as e:
            raise ValueError(f"Error retrieving cinema rooms: {str(e)}")
