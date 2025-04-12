from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud, models
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    print(f"[*] Received signup request: {user.email}")
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        print("[!] Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = crud.create_user(db, user)
    print(f"[+] New user created: {new_user.email} (ID: {new_user.userID})")
    
    return {"message": "User created successfully", "user_id": new_user.userID}

@router.post("/login/")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    print(f"[*] Login attempt: {credentials.email}")
    
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user:
        print("[!] User not found")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(credentials.password, user.password):
        print("[!] Password verification failed")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    print(f"[+] Login successful for user ID {user.userID}")
    return {"message": "Login successful", "user_id": user.userID}
