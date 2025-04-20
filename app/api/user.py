from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.db import crud, models
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password
import traceback

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    print(f"[*] Received signup request: {user.email}")
    
    try:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            print("[!] Email already registered")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user_data = user.dict()
        user_data["role"] = "inactive"
        
        new_user = crud.create_user(db, user_data)
        print(f"[+] New user created: {new_user.email} (ID: {new_user.userID})")
        
        return {"message": "User created successfully", "user_id": new_user.userID}

    except Exception as e:
        print("[!!] Exception occurred during signup:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.post("/login/")
def login(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    print(f"[*] Login attempt: {credentials.email}")
    
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user:
        print("[!] User not found")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(credentials.password, user.password):
        print("[!] Password verification failed")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    response.set_cookie(key="session_id", value=str(user.userID), httponly=True)
    print(f"[+] Login successful for user ID {user.userID}")
    return {"message": "Login successful", "user_id": user.userID}

@router.post("/logout/")
def logout(response: Response):
    """
    Endpoint to log out the user by clearing the session cookie.
    """
    response.delete_cookie(key="session_id")
    print("[+] User logged out")
    return {"message": "Logged out successfully"}




def get_current_user_from_session(request: Request, db: Session = Depends(get_db)):
    """
    Retrieve the current user from the session cookie.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = db.query(models.User).filter(models.User.userID == int(session_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    return user