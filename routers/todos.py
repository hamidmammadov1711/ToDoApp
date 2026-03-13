"""Bu kod parçacığı, FastAPI istifadə edərək bir "Todo" tətbiqinin API marşrutlarını təyin edir. Bu marşrutlar, istifadəçi doğrulaması və verilənlər bazası əməliyyatları ilə birlikdə CRUD (Yarat, Oxu, Yenilə, Sil) əməliyyatlarını həyata keçirir. Hər bir marşrut, istifadəçinin yalnız öz tapşırıqlarını görməsini və idarə etməsini təmin etmək üçün "owner_id" sahəsini yoxlayır."""

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

from dependencies import db_dependency, user_dependency
from models import Todos

router = APIRouter()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False


@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    """

    :param user:
    :param db:
    :return:
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    # İndi tapşırıqları yalnız 'owner_id' istifadəçinin ID-sinə bərabər olanlarla filtrləyirik
    return db.query(Todos).filter(Todos.owner_id == user.id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency,
              todo_id: int = Path(gt=0)):
    """

    :param user:
    :param db:
    :param todo_id:
    :return:
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    # Tapşırığı taparkən həm id-ni, həm də owner_id-ni yoxlayırıq
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.id).first())
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency,
                db: db_dependency,
                todo_request: TodoRequest):
    """

    :param user:
    :param db:
    :param todo_request:
    """
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
    """

    :param user:
    :param db:
    :param todo_request:
    :param todo_id:
    :return:
    """
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
    """

    :param user:
    :param db:
    :param todo_id:
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    # Tapşırığı taparkən həm id-ni, həm də owner_id-ni yoxlayırıq
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.id).first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    db.delete(todo_model)
    db.commit()
