from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from daos.MaintenanceRequestDAO import MaintenaceRequestDAO
from daos.UserDAO import UserDAO
from models import UserRole, MaintenanceRequest
from models import MaintenanceState


class Handler(ABC):
    def __init__(self, db: Session, next_handler: "Handler" = None):
        self._db = db
        self._next_handler = next_handler
        self.usuario_dao = UserDAO(db)
        self.request_dao = MaintenaceRequestDAO(db)

    @abstractmethod
    def handle(self, request: MaintenanceRequest, cinema_id: int) -> str:
        pass


class TechnicianHandler(Handler):
    def handle(self, request: MaintenanceRequest, cinema_id: int) -> str:
        if request.complexity == 1:
            technician = self.usuario_dao.get_available_by_role_and_cinema(
                UserRole.maintenance_technician.value, cinema_id=cinema_id
            )
            if technician:
                request.handled_by_id = technician.user_id
                update = self.request_dao.update_maintenance_request(
                    request.id, {"handled_by_id": technician.user_id, "state": MaintenanceState.assigned.value}
                )
                return update
        return (
            self._next_handler.handle(request, cinema_id)
            if self._next_handler
            else f"No se pudo asignar la solicitud {request.id}"
        )


class SupervisorHandler(Handler):
    def handle(self, request: MaintenanceRequest, cinema_id: int) -> str:
        if request.complexity == 2:
            supervisor = self.usuario_dao.get_available_by_role_and_cinema(
                UserRole.maintenance_supervisor.value, cinema_id=cinema_id
            )
            if supervisor:
                request.handled_by_id = supervisor.user_id
                update = self.request_dao.update_maintenance_request(
                    request.id, {"handled_by_id": supervisor.user_id, "state": MaintenanceState.assigned.value}
                )
                return update
        return (
            self._next_handler.handle(request, cinema_id)
            if self._next_handler
            else f"No se pudo asignar la solicitud {request.id}"
        )


class AdminHandler(Handler):
    def handle(self, request: MaintenanceRequest, cinema_id: int) -> str:
        if request.complexity == 3:
            admin = self.usuario_dao.get_available_by_role_and_cinema(UserRole.cinema_admin.value, cinema_id=cinema_id)
            if admin:
                request.handled_by_id = admin.user_id
                update = self.request_dao.update_maintenance_request(
                    request.id, {"handled_by_id": admin.user_id, "state": MaintenanceState.assigned.value}
                )
                return update
        return (
            self._next_handler.handle(request, cinema_id)
            if self._next_handler
            else f"No se pudo asignar la solicitud {request.id}"
        )
