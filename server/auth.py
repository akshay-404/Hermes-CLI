from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select
from database.models import User
from server.database import SessionLocal


password_hasher = PasswordHasher()


def register_user(username: str, password: str) -> User:
    with SessionLocal() as db:
        statement = select(User).where(
            User.username == username
        )
        existing_user = db.scalar(statement)
        if existing_user is not None:
            raise ValueError("Username already exists.")

        password_hash = password_hasher.hash(password)
        user = User(
            username=username,
            password_hash=password_hash
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


def login_user(username: str, password: str) -> User | None:
    with SessionLocal() as db:
        statement = select(User).where(
            User.username == username
        )
        user = db.scalar(statement)
        if user is None:
            return None
        try:
            password_hasher.verify(
                user.password_hash,
                password
            )
        except VerifyMismatchError:
            return None

        return user
