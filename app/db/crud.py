from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.db.models import User
from app.core.security import get_password_hash

def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
