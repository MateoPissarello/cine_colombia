from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean
import enum
from database import Base


class UserRole(enum.Enum):
    client = "client"
    admin = "admin"
    cinema_admin = "cinema_admin"
    maintenance_supervisor = "maintenance_supervisor"
    maintenance_technician = "maintenance_technician"


class days(enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"
    all = "all"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, nullable=False)
    last_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role"), default=UserRole.client)
    cinema_id = Column(Integer, ForeignKey("cinemas.id"), nullable=True)
    available = Column(Boolean, nullable=True)  # "yes" or "no"


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True)
    issue = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)  # 1: básica, 2: media, 3: alta
    handled_by_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    solved = Column(Boolean, nullable=True)
    cinema_room = Column(Integer, ForeignKey("cinema_rooms.id"), nullable=True)


class CinemaRoom(Base):
    __tablename__ = "cinema_rooms"
    id = Column(Integer, primary_key=True, index=True)
    cinema_id = Column(Integer, ForeignKey("cinemas.id"), nullable=False)
    room_number = Column(Integer, nullable=False)


class Cinema(Base):
    __tablename__ = "cinemas"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
