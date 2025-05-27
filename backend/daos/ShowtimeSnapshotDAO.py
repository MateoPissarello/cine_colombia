from sqlalchemy.orm import Session
from models import ShowtimeSnapshot


class ShowtimeSnapshotDAO:
    def __init__(self, db: Session):
        self.db = db

    def save_snapshot(self, cinema_id: int, data: dict) -> ShowtimeSnapshot:
        """
        Save a snapshot of showtimes for a specific cinema.
        """
        snapshot = ShowtimeSnapshot(cinema_id=cinema_id, data=data)
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        return snapshot

    def get_latest_snapshot(self, cinema_id: int) -> ShowtimeSnapshot | None:
        """
        Get the latest snapshot for a specific cinema.
        """
        snapshot = (
            self.db.query(ShowtimeSnapshot)
            .filter(ShowtimeSnapshot.cinema_id == cinema_id)
            .order_by(ShowtimeSnapshot.created_at.desc())
            .first()
        )
        return snapshot
