from sqlalchemy.orm import Session
from daos.TicketSaleDAO import TicketSaleDAO
from daos.CinemaDAO import CinemaDAO
from service.state.context import OccupacyContext
from models import TicketSale
from schemas.tickets_schemas import TicketSaleRetrieve


class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.ticket_dao = TicketSaleDAO(db)
        self.cinema_dao = CinemaDAO(db)

    def sell_tickets(self, sale_data: TicketSale) -> dict:
        if sale_data.tickets_sold <= 0:
            raise ValueError("You must sell at least one ticket")

        capacity = self.ticket_dao.get_showtime_capacity(sale_data.showtime_id)
        current_sold = self.ticket_dao.get_tickets_sold_by_showtime(sale_data.showtime_id)

        if current_sold + sale_data.tickets_sold > capacity:
            raise ValueError("Not enough tickets available for this showtime")
        sale = self.ticket_dao.create_ticket_sale(sale_data)

        updated_sold = current_sold + sale_data.tickets_sold
        context = OccupacyContext(updated_sold, capacity)
        return {
            "sale": TicketSaleRetrieve.model_validate(sale),
            "occupancy_state": {"label": context.state.name(), "message": context.get_state_label()},
        }

    def get_tickets_by_user(self, user_id: int) -> list[TicketSaleRetrieve]:
        """
        Retrieve all tickets sold to a specific user.
        """
        try:
            tickets = self.ticket_dao.get_tickets_by_user(user_id)
            return [TicketSaleRetrieve.model_validate(ticket) for ticket in tickets]
        except Exception as e:
            raise ValueError(f"Error retrieving tickets: {str(e)}")

    def get_tickets_by_email(self, email: str) -> list[TicketSaleRetrieve]:
        """
        Retrieve all tickets sold to a specific user by email.
        """
        try:
            tickets = self.ticket_dao.get_tickets_by_email(email)
            return [TicketSaleRetrieve.model_validate(ticket) for ticket in tickets]
        except Exception as e:
            raise ValueError(f"Error retrieving tickets: {str(e)}")
