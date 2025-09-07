from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from src.db.configurations import get_db_session
from src.db.models import User
from sqlalchemy.orm import Session
from sqlalchemy import extract, and_, or_
from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from datetime import date, timedelta

from src.api.exceptions import UserNotFoundError, DuplicateEmailError

router = APIRouter(prefix="/api/users", tags=["users"])


class UserSchema(BaseModel):
    name: str = Field(
        ..., max_length=50, description="User's first name", example="John"
    )
    surname: str = Field(
        ..., max_length=50, description="User's surname", example="Doe"
    )
    email: EmailStr = Field(
        ...,
        max_length=100,
        description="User's email address",
        example="john.doe@example.com",
    )
    birthdate: date = Field(
        ..., description="User's birthdate in YYYY-MM-DD format", example="1990-01-01"
    )
    additional_info: Optional[str] = Field(
        None, max_length=255, description="Additional information about the user"
    )


@router.get("/", response_model=list[UserSchema])
async def get_users(db: Session = Depends(get_db_session)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {e}",
        )


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchema, db: Session = Depends(get_db_session)):

    if db.query(User).filter(User.email == user.email).first():
        raise DuplicateEmailError
    try:
        new_user = User(
            name=user.name,
            surname=user.surname,
            email=user.email,
            birthdate=user.birthdate,
            additional_info=user.additional_info,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {e}",
        )


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UserNotFoundError
    return user


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, user: UserSchema, db: Session = Depends(get_db_session)
):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise UserNotFoundError
    try:
        existing_user.name = user.name
        existing_user.surname = user.surname
        existing_user.email = user.email
        existing_user.birthdate = user.birthdate
        existing_user.additional_info = user.additional_info
        db.commit()
        db.refresh(existing_user)
        return existing_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {e}",
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise UserNotFoundError
    try:
        db.delete(existing_user)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {e}",
        )


@router.get("/search/", response_model=list[UserSchema])
async def search_users(
    name: str | None = Query(None, description="Filter by name"),
    surname: str | None = Query(None, description="Filter by surname"),
    email: str | None = Query(None, description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    try:
        query = db.query(User)
        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))
        if surname:
            query = query.filter(User.surname.ilike(f"%{surname}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        users = query.all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching users: {e}",
        )


@router.get("/upcoming-birthdays/", response_model=list[UserSchema])
async def get_upcoming_birthdays(
    db: Session = Depends(get_db_session),
):
    try:
        today = date.today()
        upcoming = today + timedelta(days=7)

        users = (
            db.query(User)
            .filter(
                or_(
                    # case when birthdays are in the same month
                    and_(
                        extract("month", User.birthdate) == today.month,
                        extract("day", User.birthdate) >= today.day,
                        extract("day", User.birthdate) <= upcoming.day,
                    ),
                    # case when birthdays are in the next month
                    and_(
                        extract("month", User.birthdate) == upcoming.month,
                        extract("day", User.birthdate) <= upcoming.day,
                    ),
                )
            )
            .all()
        )
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving upcoming birthdays: {e}",
        )
