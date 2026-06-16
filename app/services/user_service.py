from database import db
from models import User


def get_or_create_auth0_user(payload):
    external_id = payload.get("sub")
    email = payload.get("email")

    if not external_id:
        raise ValueError("Auth0 token missing sub")

    user = User.query.filter_by(external_id=external_id).first()
    if user:
        return user

    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            user.external_id = external_id
            db.session.commit()
            return user

    user = User(
        email=email or f"{external_id}@auth0.local",
        password_hash=None,
        auth_provider="auth0",
        external_id=external_id,
    )

    db.session.add(user)
    db.session.commit()

    return user