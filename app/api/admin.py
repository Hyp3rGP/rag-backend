from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models, crud
from app.schemas.user import UserCreate
from app.dependencies.dependencies import get_current_admin

import os
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users/")
def get_all_users(db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """
    Endpoint for an admin to retrieve all users.
    """
    users = db.query(models.User).all()
    return {"users": users}

@router.put("/users/{userID}/role")
def change_user_role(userID: int, new_role: str, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """
    Endpoint for an admin to change the role of another user.
    """
    user = crud.get_user_by_id(db, userID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if new_role == "admin":
        raise HTTPException(status_code=400, detail="Cannot set role to admin")
    

    user.role = new_role
    db.commit()
    db.refresh(user)
    return {"message": f"User role updated to {new_role}", "userID": userID}




@router.delete("/users/{userID}")
def delete_user_account(userID: int, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    """
    Endpoint for an admin to delete (flag as deleted) a user account.
    """
    user = crud.get_user_by_id(db, userID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_deleted:
        raise HTTPException(status_code=400, detail="User account is already deleted")
    
    user.is_deleted = True
    db.commit()
    db.refresh(user)
    return {"message": f"User account deleted", "userID": userID}




UPLOAD_DIRECTORY = "/home/johndoe/Desktop/rag-backend/app/uploads/documents"



@router.post("/upload/")
def upload_document(
    file: UploadFile = File(...),
    current_admin: models.User = Depends(get_current_admin)
):
    """
    Endpoint for an admin to upload a document.
    """
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return JSONResponse(
        content={"message": f"File '{file.filename}' uploaded successfully", "file_path": file_path},
        status_code=201,
    )