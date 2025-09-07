from fastapi import APIRouter, Depends, HTTPException, status
from src.db.configurations import get_db_session
from src.db.models import User
from sqlalchemy.orm import Session
from datetime import date

from pydantic import BaseModel

router = APIRouter(prefix="/api/users", tags=["users"])


class UserSchema(BaseModel):
    name: str
    surname: str
    email: str
    birthdate: date
    additional_info: str | None


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, user: UserSchema, db: Session = Depends(get_db_session)
):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    try:
        db.delete(existing_user)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {e}",
        )
