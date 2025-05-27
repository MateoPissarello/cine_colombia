from sqlalchemy.orm import Session
from models import TicketSale, MovieShowtime, CinemaRoom


class TicketSaleDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_ticket_sale(self, ticket_sale: TicketSale) -> TicketSale:
        self.db.add(ticket_sale)
        self.db.commit()
        self.db.refresh(ticket_sale)
        return ticket_sale

    def get_tickets_sold_by_showtime(self, showtime_id: int) -> int:
        sales = self.db.query(TicketSale).filter(TicketSale.showtime_id == showtime_id).all()
        return sum(s.tickets_sold for s in sales)

    def get_showtime_capacity(self, showtime_id: int) -> int:
        showtime = self.db.query(MovieShowtime).filter(MovieShowtime.id == showtime_id).first()
        if not showtime:
            raise ValueError("Showtime not found")
        room = self.db.query(CinemaRoom).filter(CinemaRoom.id == showtime.cinema_room_id).first()
        return room.capacity if room else 0

    def get_tickets_by_user(self, user_id: int) -> list[TicketSale]:
        """
        Retrieve all tickets sold to a specific user.
        """
        return self.db.query(TicketSale).filter(TicketSale.user_id == user_id).all()

    def get_tickets_by_email(self, email: str) -> list[TicketSale]:
        """
        Retrieve all tickets sold to a specific user by email.
        """
        return self.db.query(TicketSale).filter(TicketSale.buyer_email == email).all()
