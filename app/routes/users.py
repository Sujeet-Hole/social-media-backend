from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse , LoginSchema
from app.schemas import LoginSchema, Token
from app.auth import verify_password, create_jwt_token ,get_password_hash
import logging
router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Register attempt for email : {user.email}")
    existing = db.query(User).filter(User.email == user.email).first()

    if existing :
        logger.warning(f"Email already exists : {user.email}")
        raise HTTPException(status_code=400 , detail= "email already registered")
    
    hashed = get_password_hash(user.password)
    logger.info(f"password hashed for : {user.email}")

    new_user = User(username = user.username , email = user.email , password_hash = hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created successfully")
    return new_user



@router.post("/login" , response_model=Token)

def login(user : LoginSchema , db : Session =Depends(get_db)):
    logger.info(f"login attempt for login {user.email}")
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        logger.warning(f"user not exist in database {user.email}")
        raise HTTPException(status_code=400 , detail="user not found")
    
    if not verify_password (user.password , db_user.password_hash):
        logger.warning(f"wrong password enter by user {user.email}")
        raise HTTPException(status_code=400, detail="Wrong password")
    
    token = create_jwt_token({"sub": db_user.email})
    logger.info(f"user login successfully : {user.email}")
    return {"access_token": token, "token_type": "bearer"}



@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching user: {user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"User found: {user.username}")
    return user
