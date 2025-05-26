from pydantic import BaseModel
from typing import Optional


class MaintenanceRequestRetrieve(BaseModel):
    id: int
    issue: str
    complexity: int  # 1: básica, 2: media, 3: alta
    handled_by_id: Optional[int] = None
    state: str
    solved: Optional[bool] = None  # "yes" or "no"
    cinema_room: Optional[int] = None

    model_config = {
        "from_attributes": True,
    }


class MaintenanceRequestCreate(BaseModel):
    issue: str
    complexity: int  # 1: básica, 2: media, 3: alta
    cinema_room: Optional[int] = None
