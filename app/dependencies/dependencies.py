from fastapi import Depends, HTTPException
from app.db.database import get_db
from app.db.models import User
from app.api.user import get_current_user_from_session

def get_current_admin(current_user: User = Depends(get_current_user_from_session)):
    """
    Dependency to ensure the current user is an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized as admin")
    return current_user