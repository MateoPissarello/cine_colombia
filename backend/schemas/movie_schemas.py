from pydantic import BaseModel, Field
from datetime import time
from typing import Optional


class MovieCreate(BaseModel):
    title: str = Field(..., description="The title of the movie")
    genre: str = Field(..., description="The genre of the movie")
    duration: int = Field(..., description="Duration of the movie in minutes")
    description: Optional[str] = Field(None, description="A brief description of the movie")


class MovieRetrieve(BaseModel):
    id: int = Field(..., description="The unique identifier of the movie")
    title: str = Field(..., description="The title of the movie")
    genre: str = Field(..., description="The genre of the movie")
    duration: int = Field(..., description="Duration of the movie in minutes")
    description: Optional[str] = Field(None, description="A brief description of the movie")

    model_config = {
        "from_attributes": True,
    }


class MovieShowtimeCreate(BaseModel):
    movie_id: int = Field(..., description="The ID of the movie")
    cinema_room_id: int = Field(..., description="The ID of the cinema room")
    showtime: time = Field(..., description="The start time of the showtime in ISO format")
    day_of_week: str = Field(..., description="The end time of the showtime in ISO format")


class MovieShowtimeRetrieve(BaseModel):
    id: int = Field(..., description="The unique identifier of the movie showtime")
    movie_id: int = Field(..., description="The ID of the movie")
    cinema_room_id: int = Field(..., description="The ID of the cinema room")
    showtime: time = Field(..., description="The start time of the showtime in ISO format")
    day_of_week: str = Field(..., description="The end time of the showtime in ISO format")

    model_config = {
        "from_attributes": True,
    }
