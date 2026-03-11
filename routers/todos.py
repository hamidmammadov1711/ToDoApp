from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

from dependencies import db_dependency, user_dependency
from models import Todos

router = APIRouter()


class TodoRequest(BaseModel):
    """
     This class defines a Pydantic model for a todo request. It includes fields for title, description, priority, and complete status.
     The title field is a string that represents the title of the todo item.
     The description field is a string that provides additional details about the todo item.
     The priority field is an integer that indicates the priority level of the todo item.
     The complete field is a boolean that indicates whether the todo item is completed or not, with a default value of False.
    """
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False


@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    # İndi tapşırıqları yalnız 'owner_id' istifadəçinin ID-sinə bərabər olanlarla filtrləyirik
    return db.query(Todos).filter(Todos.owner_id == user.id).all()


@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    # owner_id sahəsini istifadəçidən gələn ID ilə doldururuq
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.id)

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency,
                db: db_dependency,
                todo_request: TodoRequest,
                todo_id: int = Path(gt=0)):  # 'id' əvəzinə 'todo_id'

    # Artıq 'id' açar sözü ilə qarışıqlıq yoxdur
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.id).first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    return


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency,
                todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    # Tapşırığı taparkən həm id-ni, həm də owner_id-ni yoxlayırıq
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.id).first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    db.delete(todo_model)
    db.commit()
