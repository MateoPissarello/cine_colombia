from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as response_status
from database import get_db
from sqlalchemy.orm import Session
from service.occupancy_service import OccupancyService
from utils.get_current_user import get_current_user
from schemas.auth_schemas import TokenData
from schemas.occupancy_schemas import OccupancyStateResponse
from utils.RoleChecker import RoleChecker

router = APIRouter(prefix="/occupancy", tags=["Occupancy"])
all_users = RoleChecker(
    allowed_roles=["admin", "cinema_admin", "client", "maintenance_supervisor", "maintenance_technician"]
)


@router.get("/{showtime_id}", response_model=OccupancyStateResponse, status_code=response_status.HTTP_200_OK)
async def get_occupancy_info(
    showtime_id: int,
    db: Session = Depends(get_db),
    role_checker: RoleChecker = Depends(all_users),
    current_user: TokenData = Depends(get_current_user),
):
    """
    Get the occupancy state of a movie showtime.
    """
    service = OccupancyService(db)
    try:
        occupancy_info = service.get_occupancy_info(showtime_id)
        return occupancy_info
    except ValueError as e:
        raise HTTPException(status_code=response_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
