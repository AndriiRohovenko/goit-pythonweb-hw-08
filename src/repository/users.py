from sqlalchemy.orm import Session
from sqlalchemy import extract, and_, or_
from datetime import date, timedelta
from src.db.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, existing_user: User, data: dict):
        for field, value in data.items():
            setattr(existing_user, field, value)
        self.db.commit()
        self.db.refresh(existing_user)
        return existing_user

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()

    def search(self, name: str | None, surname: str | None, email: str | None):
        query = self.db.query(User)
        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))
        if surname:
            query = query.filter(User.surname.ilike(f"%{surname}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        return query.all()

    def upcoming_birthdays(self):
        today = date.today()
        upcoming = today + timedelta(days=7)

        return (
            self.db.query(User)
            .filter(
                or_(
                    and_(
                        extract("month", User.birthdate) == today.month,
                        extract("day", User.birthdate) >= today.day,
                        extract("day", User.birthdate) <= upcoming.day,
                    ),
                    and_(
                        extract("month", User.birthdate) == upcoming.month,
                        extract("day", User.birthdate) <= upcoming.day,
                    ),
                )
            )
            .all()
        )
