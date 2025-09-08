from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from src.db.configurations import get_db_session
from src.db.models import User
from sqlalchemy.orm import Session
from sqlalchemy import extract, and_, or_
from typing import Optional


from datetime import date, timedelta

from src.api.exceptions import UserNotFoundError, DuplicateEmailError, ServerError

from src.schemas.users import UserSchema
from src.services.users import UserService
from src.repository.users import UserRepository

router = APIRouter(prefix="/api/users", tags=["users"])


def get_service(db: Session = Depends(get_db_session)):
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/", response_model=list[UserSchema])
async def get_users(service: UserService = Depends(get_service)):
    return service.get_users()


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchema, service: UserService = Depends(get_service)):
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, service: UserService = Depends(get_service)):
    return service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, user: UserSchema, service: UserService = Depends(get_service)
):
    user = service.update_user(user_id, user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_service)):
    service.delete_user(user_id)


@router.get("/search/", response_model=list[UserSchema])
async def search_users(
    name: str | None = Query(None, description="Filter by name"),
    surname: str | None = Query(None, description="Filter by surname"),
    email: str | None = Query(None, description="Filter by email"),
    service: UserService = Depends(get_service),
):
    return service.search_users(name, surname, email)


@router.get("/upcoming-birthdays/", response_model=list[UserSchema])
async def get_upcoming_birthdays(service: UserService = Depends(get_service)):

    return service.upcoming_birthdays()
