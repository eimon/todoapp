from fastapi import Depends, Path, HTTPException,APIRouter
from typing import Annotated, Optional
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: Optional[bool] = False

@router.get("/", status_code=status.HTTP_200_OK)
def all_tareas(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()

@router.get("/{id_todo}", status_code=status.HTTP_200_OK)
def read_todo(user:user_dependency, db: db_dependency, id_todo: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    todo_model = db.query(Todos).filter(Todos.id==id_todo).filter(Todos.owner_id==user.get('get')).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="No se encontró el quehacer.")
    
@router.post("/crear_todo/", status_code=status.HTTP_201_CREATED)
def crear_todo(user:user_dependency, db: db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    todo_model=Todos(**todo_request.dict(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user:user_dependency, db: db_dependency, todo_request:TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('get')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="No se encontró el quehacer.")
    
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    db.commit()

@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependency, db:db_dependency,todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('get')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="No se encontró el quehacer")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('get')).delete()
    db.commit()

