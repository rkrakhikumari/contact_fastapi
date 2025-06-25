from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from database import SessionLocal
from .auth import get_db, verify_password, get_password_hash, create_access_token
from schemas import UserCreate, UserLogin
from models import User
from database import SessionLocal


router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/register',status_code= status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: db_dependency):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='email already register')
    hased_pw = get_password_hash(user.password)
    new_user = User(name = user.name, email = user.email, password = hased_pw)
    db.add(new_user)
    db.commit()
    return {'msg': 'user created successfuly'}



@router.post('/login')
def login_user(user: UserLogin, db: db_dependency):
    db_user = db.query(User).filter(User.name == user.name).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail= "invalid user or password")
    token = create_access_token(data={'sub': str(db_user.id)})
    return {'access_toke': token, 'type': 'bearer'}

