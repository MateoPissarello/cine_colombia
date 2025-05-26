from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.maintenance_schemas import MaintenanceRequestCreate, MaintenanceRequestRetrieve
from fastapi import status as status_code, Body
from schemas.auth_schemas import TokenData
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from service.maintenance_service import MaintenanceService
from models import MaintenanceRequest
from typing import List

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
        data = MaintenanceRequest(**request_data.model_dump(exclude_unset=True))
        return service.create_maintenance_request(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/request/process/{request_id}", response_model=MaintenanceRequestRetrieve, status_code=status_code.HTTP_200_OK
)
async def process_maintenance_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(employee_only),
):
    """
    Process a maintenance request.
    """
    service = MaintenanceService(db)
    try:
        return service.process_maintenance_request(request_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/requests/cinema/{cinema_id}",
    response_model=List[MaintenanceRequestRetrieve],
    status_code=status_code.HTTP_200_OK,
)
async def get_maintenance_requests_by_cinema(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(employee_only),
):
    """
    Get all maintenance requests for a specific cinema.
    """
    service = MaintenanceService(db)
    try:
        return service.get_maintenace_requests_by_cinema(cinema_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
