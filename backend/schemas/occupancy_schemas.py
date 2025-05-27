from pydantic import BaseModel, Field


class OccupancyStateResponse(BaseModel):
    showtime_id: int = Field(..., description="The ID of the movie showtime")
    tickets_sold: int = Field(..., description="Number of tickets sold for the showtime")
    room_capacity: int = Field(..., description="Total capacity of the cinema room for the showtime")
    occupancy_percentage: float = Field(..., description="Percentage of occupancy for the showtime")
    state: str = Field(..., description="Current occupancy state of the showtime (Available, Almost Full, Full)")
    message: str = Field(..., description="Message describing the occupancy state")

    model_config = {
        "from_attributes": True,
    }
