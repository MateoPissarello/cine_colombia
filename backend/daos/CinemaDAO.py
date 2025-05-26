from sqlalchemy.orm import Session
from models import Cinema, CinemaRoom


class CinemaDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_cinema(self, request_data: Cinema) -> Cinema:
        self.db.add(request_data)
        self.db.commit()
        self.db.refresh(request_data)
        return request_data

    def create_cinema_room(self, request_data: CinemaRoom) -> CinemaRoom:
        self.db.add(request_data)
        self.db.commit()
        self.db.refresh(request_data)
        return request_data

    def get_cinema_room_by_number(self, cinema_id: int, room_number: int) -> CinemaRoom | None:
        cinema_room = (
            self.db.query(CinemaRoom)
            .filter(CinemaRoom.cinema_id == cinema_id, CinemaRoom.room_number == room_number)
            .first()
        )
        return cinema_room

    def get_rooms_by_cinema_id(self, cinema_id: int) -> list[CinemaRoom]:
        cinema_rooms = self.db.query(CinemaRoom).filter(CinemaRoom.cinema_id == cinema_id).all()
        return cinema_rooms

    def get_cinema_room(self, cinema_room_id: int) -> CinemaRoom:
        cinema_room = self.db.query(CinemaRoom).filter(CinemaRoom.id == cinema_room_id).first()
        return cinema_room

    def update_cinema(self, cinema_id: int, updated_data: dict) -> Cinema | None:
        cinema = self.get_schedule(cinema_id)
        if cinema:
            for key, value in updated_data.items():
                setattr(cinema, key, value)
            self.db.commit()
            self.db.refresh(cinema)
            return cinema
        return None

    def delete_cinema(self, cinema_id: int) -> bool:
        cinema_id = self.get_schedule(cinema_id)
        if cinema_id:
            self.db.delete(cinema_id)
            self.db.commit()
            return True
        return False

    def get_cinema(self, cinema_id: int) -> Cinema | None:
        cinema = self.db.query(Cinema).filter(Cinema.id == cinema_id).first()
        return cinema
