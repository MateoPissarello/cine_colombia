from sqlalchemy.orm import Session
from models import MaintenanceRequest


class MaintenaceRequestDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_maintenance_request(self, request_data: MaintenanceRequest) -> MaintenanceRequest:
        self.db.add(request_data)
        self.db.commit()
        self.db.refresh(request_data)
        return request_data

    def update_maintenance_request(self, maintenance_request_id: int, updated_data: dict) -> MaintenanceRequest | None:
        maintenance = self.get_schedule(maintenance_request_id)
        if maintenance:
            for key, value in updated_data.items():
                setattr(maintenance, key, value)
            self.db.commit()
            self.db.refresh(maintenance)
            return maintenance
        return None

    def delete_maintenance_request(self, maintenance_request_id: int) -> bool:
        maintenance_request_id = self.get_schedule(maintenance_request_id)
        if maintenance_request_id:
            self.db.delete(maintenance_request_id)
            self.db.commit()
            return True
        return False

    def get_maintenance_request(self, maintenance_request_id: int) -> MaintenanceRequest | None:
        maintenance = self.db.query(MaintenanceRequest).filter(MaintenanceRequest.id == maintenance_request_id).first()
        return maintenance
