from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from daos.MaintenanceRequestDAO import MaintenaceRequestDAO
from daos.UserDAO import UserDAO
from models import UserRole, MaintenanceRequest


class Handler(ABC):
    def __init__(self, db: Session, next_handler: "Handler" = None):
        self._db = db
        self._next_handler = next_handler
        self.usuario_dao = UserDAO(db)
        self.request_dao = MaintenaceRequestDAO(db)

    @abstractmethod
    def handle(self, request: MaintenanceRequest) -> str:
        pass


class TechnicianHandler(Handler):
    def handle(self, request: MaintenanceRequest) -> str:
        if request.complexity == 1:
            technician = self.usuario_dao.get_available_by_role_and_cinema(
                UserRole.maintenance_technician, cinema_id=request.cinema_room.cinema_id
            )
            if technician:
                request.handled_by_id = technician.id
                self.request_dao.update_maintenance_request(request.id, {"handled_by_id": technician.id})
                return f"Técnico {technician.first_name} fue asignado a la solicitud {request.id}"
        return (
            self._next_handler.handle(request)
            if self._next_handler
            else f"No se pudo asignar la solicitud {request.id}"
        )


class SupervisorHandler(Handler):
    def handle(self, request: MaintenanceRequest) -> str:
        if request.complexity == 2:
            supervisor = self.usuario_dao.get_available_by_role_and_cinema(
                UserRole.maintenance_supervisor, cinema_id=request.cinema_room.cinema_id
            )
            if supervisor:
                request.handled_by_id = supervisor.id
                self.request_dao.update_maintenance_request(request.id, {"handled_by_id": supervisor.id})
                return f"Supervisor {supervisor.first_name} fue asignado a la solicitud {request.id}"
        return (
            self._next_handler.handle(request)
            if self._next_handler
            else f"No se pudo asignar la solicitud {request.id}"
        )


class AdminHandler(Handler):
    def handle(self, request: MaintenanceRequest) -> str:
        if request.complexity == 3:
            admin = self.usuario_dao.get_available_by_role_and_cinema(
                UserRole.cinema_admin, cinema_id=request.cinema_room.cinema_id
            )
            if admin:
                request.handled_by_id = admin.id
                self.request_dao.update_maintenance_request(request.id, {"handled_by_id": admin.id})
                return f"Administrador {admin.first_name} aprobó la solicitud {request.id}"
        return (
            self._next_handler.handle(request)
            if self._next_handler
            else f"No se pudo asignar la solicitud {request.id}"
        )
