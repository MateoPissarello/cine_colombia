from daos.ShowtimeSnapshotDAO import ShowtimeSnapshotDAO
from .memento import ShowtimeMemento


class SnapshotCaretaker:
    def __init__(self, snapshot_dao: ShowtimeSnapshotDAO):
        self.snapshot_dao = snapshot_dao

    def store_snapshot(self, cinema_id: int, memento: ShowtimeMemento):
        self.snapshot_dao.save_snapshot(cinema_id, memento.get_state())

    def retrieve_latest_snapshot(self, cinema_id: int) -> ShowtimeMemento:
        snapshot = self.snapshot_dao.get_latest_snapshot(cinema_id)
        if not snapshot:
            raise ValueError("No hay snapshot disponible")
        return ShowtimeMemento(snapshot.data)
