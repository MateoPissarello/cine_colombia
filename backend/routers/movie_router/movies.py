from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi import status as response_status
from service.movie_service import MovieService
from sqlalchemy.orm import Session
from schemas.auth_schemas import TokenData
from schemas.movie_schemas import MovieShowtimeRetrieve, MovieRetrieve, MovieCreate, MovieShowtimeCreate
from utils.get_current_user import get_current_user
from utils.RoleChecker import RoleChecker
from database import get_db
from models import days, Movie, MovieShowtime
from typing import List

router = APIRouter(prefix="/movies", tags=["Movies"])


employee_only = RoleChecker(allowed_roles=["admin", "cinema_admin", "maintenance_supervisor", "maintenance_technician"])
only_admins = RoleChecker(allowed_roles=["admin", "cinema_admin"])
all_users = RoleChecker(
    allowed_roles=["admin", "cinema_admin", "client", "maintenance_supervisor", "maintenance_technician"]
)


@router.get("/", response_model=List[MovieRetrieve], status_code=response_status.HTTP_200_OK)
async def get_all_movies(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(all_users),
):
    """
    Get all movies.
    """
    service = MovieService(db)
    try:
        movies = service.get_movies()
        if not movies:
            raise HTTPException(status_code=response_status.HTTP_404_NOT_FOUND, detail="No movies found.")
        return movies
    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", status_code=response_status.HTTP_201_CREATED, response_model=MovieRetrieve)
async def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(only_admins),
):
    """
    Create a new movie.
    """
    service = MovieService(db)
    try:
        data = Movie(**movie.model_dump(exclude_unset=True))
        created_movie = service.create_movie(data)
        return created_movie
    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/showtime", response_model=MovieShowtimeRetrieve, status_code=response_status.HTTP_201_CREATED)
async def create_showtime(
    request_data: MovieShowtimeCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(employee_only),
):
    """
    Create a new movie showtime.
    """
    service = MovieService(db)
    try:
        data = MovieShowtime(**request_data.model_dump(exclude_unset=True))
        showtime = service.create_showtime(data)
        return showtime
    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/showtimes/{cinema_id}", response_model=List[MovieShowtimeRetrieve], status_code=response_status.HTTP_200_OK
)
async def get_showtimes_by_cinema(
    cinema_id: int,
    db: Session = Depends(get_db),
    day: days = Query(default=None, description="Filter by day of the week"),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(all_users),
):
    """
    Get all movie showtimes for a specific cinema.
    """
    service = MovieService(db)
    try:
        iterator = service.get_showtimes_iterator_for_cinema(cinema_id)
        if day:
            iterator = iterator.filter_by_day(day)
        showtimes = list(iterator)
        if not showtimes:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="No showtimes found for the specified cinema.",
            )
        return showtimes

    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
