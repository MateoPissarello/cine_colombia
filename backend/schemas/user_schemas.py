from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class CreateUserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=50)
    role: str = Field(..., min_length=1, max_length=50)
    cinema_id: Optional[int] = Field(None, ge=1)
    available: Optional[bool] = Field(None)  # True or False

    @model_validator(mode="after")
    def check_role(self):
        if self.role not in ["admin", "cinema_admin", "client", "maintenance_supervisor", "maintenance_technician"]:
            raise ValueError(
                "Role must be either 'client', 'admin', 'cinema_admin', 'maintenance_supervisor', or 'maintenance_technician'"
            )
        if self.role in ["cinema_admin", "maintenance_supervisor", "maintenance_technician"] and self.cinema_id is None:
            raise ValueError("Cinema ID must be provided for cinema-related roles")
        return self


class RetrieveUserBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    cinema_id: Optional[int] = None
    available: Optional[bool] = None  # "yes" or "no"

    model_config = {"from_attributes": True}


class UpdateUserBase(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    available: Optional[bool] = Field(None)  # True or False


class UpdateUserBaseAdmin(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    role: Optional[str] = Field(None, min_length=1, max_length=50)
    cinema_id: Optional[int] = Field(None, ge=1)
