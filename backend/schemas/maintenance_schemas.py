from pydantic import BaseModel, EmailStr
from typing import Optional


class RetrieveCinema(BaseModel):
    id: int
    nombre: str
    direccion: str

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

    model_config = {
        "from_attributes": True,
    }


class CinemaRoomCreate(BaseModel):
    cinema_id: int
    room_number: int


class MaintenanceRequestRetrieve(BaseModel):
    id: int
    issue: str
    complexity: int  # 1: básica, 2: media, 3: alta
    handled_by_id: Optional[int] = None
    solved: Optional[bool] = None  # "yes" or "no"
    cinema_room: Optional[int] = None

    model_config = {
        "from_attributes": True,
    }


class MaintenanceRequestCreate(BaseModel):
    issue: str
    complexity: int  # 1: básica, 2: media, 3: alta
    handled_by_id: Optional[int] = None
    solved: Optional[bool] = None  # "yes" or "no"
    cinema_room: Optional[int] = None
