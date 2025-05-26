from sqlalchemy.orm import Session
from daos.MaintenanceRequestDAO import MaintenaceRequestDAO
from handlers.maintenance_chain import TechnicianHandler, SupervisorHandler, AdminHandler
from schemas.maintenance_schemas import MaintenanceRequestRetrieve


class MaintenanceService:
    def __init__(self, db: Session):
        self.db = db
        self.request_dao = MaintenaceRequestDAO(db)

        # Set up the chain of responsibility

    def process_maintenance_request(self, request_id: int) -> MaintenanceRequestRetrieve:
        request = self.request_dao.get_maintenance_request(request_id)

        admin_handler = AdminHandler(self.db)
        supervisor_handler = SupervisorHandler(self.db, next_handler=admin_handler)
        technician_handler = TechnicianHandler(self.db, next_handler=supervisor_handler)

        return technician_handler.handle(request)

    def create_maintenance_request(self, request_data: dict) -> MaintenanceRequestRetrieve:
        data = self.request_dao.create_maintenance_request(request_data)
        return data
