from fastapi import Depends, Path, HTTPException,APIRouter
from typing import Annotated, Optional
from models import Users
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user, bcrypt_context

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
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get("/current_user", status_code=status.HTTP_200_OK)
def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=201, detail='Autenticación fallida')
    return db.query(Users).filter(Users.id==user.get('id')).first()

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(user:user_dependency, db:db_dependency, user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Verificación fallida")
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.commit()