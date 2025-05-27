from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class TicketSaleCreate(BaseModel):
    showtime_id: int = Field(..., description="The ID of the movie showtime")
    tickets_sold: int = Field(..., description="Number of tickets to be sold", gt=0)
    user_id: Optional[int] = Field(None, description="ID of the user making the purchase")
    buyer_name: Optional[str] = Field(None, description="Name of the buyer")
    buyer_email: Optional[EmailStr] = Field(None, description="Email of the buyer")
    buyer_phone: Optional[str] = Field(None, description="Phone number of the buyer")


class TicketSaleRetrieve(BaseModel):
    id: int = Field(..., description="The unique identifier of the ticket sale")
    showtime_id: int = Field(..., description="The ID of the movie showtime")
    tickets_sold: int = Field(..., description="Number of tickets sold")
    user_id: Optional[int] = Field(None, description="ID of the user who made the purchase")
    buyer_name: Optional[str] = Field(None, description="Name of the buyer")
    buyer_email: Optional[EmailStr] = Field(None, description="Email of the buyer")
    buyer_phone: Optional[str] = Field(None, description="Phone number of the buyer")
    purchase_time: datetime = Field(..., description="Timestamp of the purchase")

    model_config = {
        "from_attributes": True,
    }
