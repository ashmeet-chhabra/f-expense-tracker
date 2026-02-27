from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from database import get_db
from models import UserModel
from schemas import UserCreate, UserResponse
from auth import hash_password

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post('/register', response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):    

    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if(existing_user):
       raise HTTPException(detail="Email already registered", status_code=400)
       
    db_user = UserModel(
         name = user.name,
         email = user.email,
         hashed_password = hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user) 

    return db_user