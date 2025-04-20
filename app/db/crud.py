from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.db.models import User
from app.core.security import get_password_hash

def create_user(db: Session, user_data: dict):
    """
    Create a new user in the database.
    """
    db_user = User(
        name=user_data["name"],
        email=user_data["email"],
        password=get_password_hash(user_data["password"]),
        role=user_data["role"],
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    """
    Retrieve a user by their ID.
    """
    return db.query(User).filter(User.userID == user_id).first()