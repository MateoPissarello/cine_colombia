from pydantic import BaseModel, EmailStr, Field


class RetrieveCinema(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    email: EmailStr

    model_config = {
        "from_attributes": True,
    }


class CinemaCreate(BaseModel):
    name: str
    address: str
    phone: str
    email: EmailStr


class CinemaRoomRetrieve(BaseModel):
    id: int
    cinema_id: int
    room_number: int
    capacity: int

    model_config = {
        "from_attributes": True,
    }


class CinemaRoomCreate(BaseModel):
    cinema_id: int
    room_number: int = Field(..., ge=1, description="Room number must be greater than or equal to 1")
    capacity: int = Field(..., ge=1, description="Capacity must be greater than or equal to 1")
