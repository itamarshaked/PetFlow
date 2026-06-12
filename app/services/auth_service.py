import bcrypt

from database import db
from models import User


def create_user(email: str, password: str) -> User:
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(
        email=email,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return user


def verify_user(email: str, password: str) -> User | None:
    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return None

    return user
