from sqlalchemy.orm import Session
from models import Cinema


class CinemaDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_maintenance_request(self, request_data: Cinema) -> Cinema:
        self.db.add(request_data)
        self.db.commit()
        self.db.refresh(request_data)
        return request_data

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
