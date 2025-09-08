from src.repository.users import UserRepository
from src.db.models import User
from src.api.exceptions import UserNotFoundError, DuplicateEmailError, ServerError


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_users(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise ServerError from e

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        try:
            return user
        except Exception as e:
            raise ServerError from e

    def create_user(self, data):
        if self.repo.get_by_email(data.email):
            raise DuplicateEmailError
        try:
            new_user = User(**data.dict())
            return self.repo.create(new_user)
        except Exception as e:
            raise ServerError from e

    def update_user(self, user_id: int, data):
        existing = self.repo.get_by_id(user_id)
        if not existing or existing is None:
            raise UserNotFoundError
        if self.repo.get_by_email(data.email) and existing.email != data.email:
            raise DuplicateEmailError
        try:
            return self.repo.update(existing, data.dict())
        except Exception as e:
            raise ServerError from e

    def delete_user(self, user_id: int):
        existing = self.repo.get_by_id(user_id)
        if not existing or existing is None:
            raise UserNotFoundError
        try:
            self.repo.delete(existing)
        except Exception as e:
            raise ServerError from e

    def search_users(self, name, surname, email):
        try:
            return self.repo.search(name, surname, email)
        except Exception as e:
            raise ServerError from e

    def upcoming_birthdays(self):
        try:
            return self.repo.upcoming_birthdays()
        except Exception as e:
            raise ServerError from e
