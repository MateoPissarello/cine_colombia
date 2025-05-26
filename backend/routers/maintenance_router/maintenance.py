from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.maintenance_schemas import MaintenanceRequestCreate, MaintenanceRequestRetrieve
from fastapi import status as status_code, Body
from schemas.auth_schemas import TokenData
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from service.maintenance_service import MaintenanceService

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

employee_only = RoleChecker(allowed_roles=["admin", "cinema_admin", "maintenance_supervisor", "maintenance_technician"])


@router.post("/request", response_model=MaintenanceRequestRetrieve, status_code=status_code.HTTP_201_CREATED)
async def create_maintenance_request(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(employee_only),
    request_data: MaintenanceRequestCreate = Body(...),
):
    """
    Create a new maintenance request.
    """
    service = MaintenanceService(db)
    try:
        return service.create_maintenance_request(request_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
