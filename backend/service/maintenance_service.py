from sqlalchemy.orm import Session
from daos.MaintenanceRequestDAO import MaintenaceRequestDAO
from daos.CinemaDAO import CinemaDAO
from handlers.maintenance_chain import TechnicianHandler, SupervisorHandler, AdminHandler
from schemas.maintenance_schemas import MaintenanceRequestRetrieve
from models import MaintenanceRequest


class MaintenanceService:
    def __init__(self, db: Session):
        self.db = db
        self.request_dao = MaintenaceRequestDAO(db)
        self.cinema_dao = CinemaDAO(db)

        # Set up the chain of responsibility

    def process_maintenance_request(self, request_id: int) -> MaintenanceRequestRetrieve:
        request = self.request_dao.get_maintenance_request(request_id)
        if request.state.value != "created":
            raise ValueError("Maintenance request is not in a processable state")
        if request is None:
            raise ValueError("Maintenance request does not exist")
        cinema_room = self.cinema_dao.get_cinema_room(request.cinema_room)
        cinema_id = cinema_room.cinema_id

        admin_handler = AdminHandler(self.db)
        supervisor_handler = SupervisorHandler(self.db, next_handler=admin_handler)
        technician_handler = TechnicianHandler(self.db, next_handler=supervisor_handler)

        return technician_handler.handle(request, cinema_id)

    def create_maintenance_request(self, request_data: MaintenanceRequest) -> MaintenanceRequestRetrieve:
        if self.cinema_dao.get_cinema_room(request_data.cinema_room) is None:
            raise ValueError("Cinema room does not exist")
        data = self.request_dao.create_maintenance_request(request_data)
        return data

    def get_maintenace_requests_by_cinema(self, cinema_id: int) -> list[MaintenanceRequestRetrieve]:
        if not self.cinema_dao.get_cinema(cinema_id):
            raise ValueError("Cinema with this ID does not exist")
        requests = self.request_dao.get_maintenance_requests_by_cinema(cinema_id)
        return requests

    def cinema_id_of_maintenance_request(self, request_id: int) -> int:
        request = self.request_dao.get_maintenance_request(request_id)
        if request is None:
            raise ValueError("Maintenance request does not exist")
        return request.cinema_room.cinema_id
