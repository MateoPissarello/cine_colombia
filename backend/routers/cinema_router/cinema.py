from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.cinema_schemas import CinemaRoomRetrieve, CinemaCreate, CinemaRoomCreate, RetrieveCinema
from fastapi import status as status_code, Body
from schemas.auth_schemas import TokenData
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from service.cinema_service import CinemaService
from models import Cinema, CinemaRoom

router = APIRouter(prefix="/cinema", tags=["Cinema"])

employee_only = RoleChecker(allowed_roles=["admin", "cinema_admin", "maintenance_supervisor", "maintenance_technician"])
all_users = RoleChecker(allowed_roles=["admin", "cinema_admin", "client", "maintenance_supervisor", "maintenance_technician"])

@router.post("/", response_model=RetrieveCinema, status_code=status_code.HTTP_201_CREATED)
async def create_cinema(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(employee_only),
    request_data: CinemaCreate = Body(...),
):
    """
    Create a new maintenance request.
    """
    service = CinemaService(db)
    try:
        data = Cinema(**request_data.model_dump(exclude_unset=True))
        return service.create_cinema(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/room", response_model=CinemaRoomRetrieve, status_code=status_code.HTTP_201_CREATED)
async def create_cinema_room(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(employee_only),
    request_data: CinemaRoomCreate = Body(...),
):
    """
    Create a new cinema room.
    """
    service = CinemaService(db)
    try:
        data = CinemaRoom(**request_data.model_dump(exclude_unset=True))
        return service.create_cinema_room(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rooms/{cinema_id}", response_model=list[CinemaRoomRetrieve], status_code=status_code.HTTP_200_OK)
async def get_cinema_rooms_by_cinema_id(
    cinema_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(all_users),
):
    """
    Get all cinema rooms by cinema ID.
    """
    service = CinemaService(db)
    try:
        return service.get_cinema_rooms_by_cinema_id(cinema_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
