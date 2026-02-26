from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse , LoginSchema
from app.schemas import LoginSchema, Token
from app.auth import verify_password, create_jwt_token ,get_password_hash
router = APIRouter()
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(user.email == user.email)

    if existing :
        raise HTTPException(status_code=400 , detail= "email already registered")
    
    hashed = get_password_hash(user.password)

    new_user = User(username = user.username , email = user.email , hashed_password = hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login" , response_model=Token)
def login(user : LoginSchema , db : Session =Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=400 , detail="user not found")
    
    if not verify_password (user.password , db_user.password_hash):
        raise HTTPException(status_code=400, detail="Wrong password")

        
    token = create_jwt_token({"sub": db_user.email})
    
    return {"access_token": token, "token_type": "bearer"}
