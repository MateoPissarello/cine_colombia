from sqlalchemy.orm import Session
from daos.MovieDAO import MovieDAO
from daos.TicketSaleDAO import TicketSaleDAO
from service.state.context import OccupacyContext
from schemas.occupancy_schemas import OccupancyStateResponse


class OccupancyService:
    def __init__(self, db: Session):
        self.db = db
        self.movie_dao = MovieDAO(db)
        self.ticket_sale_dao = TicketSaleDAO(db)

    def get_occupancy_info(self, showtime_id: int) -> OccupancyStateResponse:
        """
        Get the occupancy state of a movie showtime.
        """
        try:
            showtime = self.movie_dao.get_showtime_by_id(showtime_id)
            if not showtime:
                raise ValueError("Showtime does not exist")

            # Get the total tickets sold for the showtime
            tickets_sold = self.ticket_sale_dao.get_tickets_sold_by_showtime(showtime_id)
            # Get the showtime capacity
            room_capacity = self.ticket_sale_dao.get_showtime_capacity(showtime_id)

            if room_capacity == 0:
                raise ValueError("Showtime capacity is zero, cannot determine occupancy")

            # Create occupancy context to determine state
            context = OccupacyContext(tickets_sold, room_capacity)
            state_label = context.get_state_label()

            return OccupancyStateResponse(
                showtime_id=showtime_id,
                tickets_sold=tickets_sold,
                room_capacity=room_capacity,
                occupancy_percentage=round((tickets_sold / room_capacity) * 100, 2),
                state=context.state.name(),
                message=state_label,
            )
        except Exception as e:
            raise ValueError(f"Error retrieving occupancy info: {str(e)}")
