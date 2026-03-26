"""This module defines special endpoints for users with the "admin" role using FastAPI."""

from fastapi import APIRouter, HTTPException, Path
from starlette import status

from dependencies import db_dependency, user_dependency
from models import Todos

router = APIRouter(
    prefix='/admin',
    tags=['🐱‍👤 admin']
)


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    """Returns all todos (admin only)."""
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    """Todo will be deleted (by the admin only)."""
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
