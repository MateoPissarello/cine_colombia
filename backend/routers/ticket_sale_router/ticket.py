from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as response_status
from database import get_db
from sqlalchemy.orm import Session
from service.ticket_service import TicketService
from utils.get_current_user import get_current_user
from schemas.auth_schemas import TokenData
from schemas.tickets_schemas import TicketSaleCreate, TicketSaleRetrieve
from utils.RoleChecker import RoleChecker
from models import TicketSale
from fastapi import Query
from typing import Optional
from typing import List

router = APIRouter(prefix="/ticket", tags=["Ticket Sale"])
all_users = RoleChecker(
    allowed_roles=["admin", "cinema_admin", "client", "maintenance_supervisor", "maintenance_technician"]
)


@router.post("/buy", status_code=response_status.HTTP_200_OK)
async def get_occupancy_info(
    sale_data: TicketSaleCreate,
    db: Session = Depends(get_db),
    role_checker: RoleChecker = Depends(all_users),
    current_user: TokenData = Depends(get_current_user),
):
    """
    Get the occupancy state of a movie showtime.
    """
    service = TicketService(db)
    try:
        data = TicketSale(**sale_data.model_dump())
        return service.sell_tickets(data)
    except ValueError as e:
        raise HTTPException(status_code=response_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/my/tickets", status_code=response_status.HTTP_200_OK, response_model=List[TicketSaleRetrieve])
async def get_tickets_by_user(
    by_email: Optional[bool] = Query(False, description="Filter tickets by email if True, otherwise by user ID"),
    email: Optional[str] = Query(None, description="email to filter tickets by"),
    db: Session = Depends(get_db),
    role_checker: RoleChecker = Depends(all_users),
    current_user: TokenData = Depends(get_current_user),
):
    """
    Retrieve all tickets sold to the current user.
    """
    service = TicketService(db)
    try:
        if by_email:
            if not email:
                raise HTTPException(
                    status_code=response_status.HTTP_400_BAD_REQUEST, detail="Email is required when filtering by email"
                )
            return service.get_tickets_by_email(email)
        else:
            return service.get_tickets_by_user(current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=response_status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
