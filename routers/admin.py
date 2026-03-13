from fastapi import APIRouter, HTTPException, Path
from starlette import status

from dependencies import db_dependency, user_dependency
from models import Todos

router = APIRouter(
    prefix='/admin',
    tags=['👑 admin']
)


@router.get("/todos", status_code=status.HTTP_200_OK)
def read_all_todos(user: user_dependency, db: db_dependency):
    """
    Bu endpoint, bütün tapşırıqları (todos) əldə etmək üçün istifadə olunur. Yalnız "admin" roluna sahib olan istifadəçilər bu endpointə daxil ola bilərlər. Endpoint, verilənlər bazasından bütün tapşırıqları çəkir və onları JSON formatında geri qaytarır. Əgər istifadəçi "admin" deyilsə, HTTP 403 Forbidden status kodu ilə bir xəta mesajı qaytarılır.
    :param user: Cari istifadəçi məlumatlarını ehtiva edən obyekt.
    :param db: Verilənlər bazası sessiyası.
    :return: Bütün tapşırıqların siyahısı və ya bir xəta mesajı.
    """
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to access this resource")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_admin(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    """

    :param user:
    :param db:
    :param todo_id:
    """
    if user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
