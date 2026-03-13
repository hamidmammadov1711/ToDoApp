"""Bu modul, FastAPI istifadə edərək "admin" roluna sahib istifadəçilər üçün xüsusi endpointləri tanımlar. Bu endpointler, yalnız admin" roluna sahip kullanıcıların erişebileceği işlemleri içerir. Örneğin, tüm tapşırıqları (todos) görüntüleme ve belirli bir tapşırığı silme gibi işlemler bu modül altında tanımlanır. Endpointler, kullanıcıların yetkilerini kontrol eder ve uygun HTTP durum kodları ile yanıt verir."""
from fastapi import APIRouter, HTTPException, Path
from starlette import status

from dependencies import db_dependency, user_dependency
from models import Todos

router = APIRouter(
    prefix='/admin',
    tags=['🐱‍👤 admin']
)


@router.get("/todos", status_code=status.HTTP_200_OK)
def read_all_todos(user: user_dependency, db: db_dependency):
    """
    Bu endpoint, bütün tapşırıqları (todos) əldə etmək üçün istifadə olunur. Yalnız "admin" roluna sahib olan istifadəçilər bu endpointə daxil ola bilərlər. Endpoint, verilənlər bazasından bütün tapşırıqları çəkir və onları JSON formatında geri qaytarır. Əgər istifadəçi "admin" deyilsə, HTTP 403 Forbidden status kodu ilə bir xəta mesajı qaytarılır.
    :param user: Cari istifadəçi məlumatlarını ehtiva edən obyekt.
    :param db: Verilənlər bazası sessiyası.
    :return: Bütün tapşırıqların siyahısı və ya bir xəta mesajı.
    """
    if user is None or user.role.lower() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to access this resource")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_admin(user: user_dependency,
                         db: db_dependency,
                         todo_id: int = Path(gt=0)):
    """

    :param user:
    :param db:
    :param todo_id:
    """
    # 1. İlk öncə icazəni yoxlayırıq
    if user.role.lower() != "admin":
        raise HTTPException(status_code=status.HTTP_401_FORBIDDEN,
                            detail="Admin access required")

    # 2. Tapşırığı tapırıq (sahibindən asılı olmayaraq)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    # 3. Tapşırıq mövcud deyilsə xəta veririk
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # 4. Silirik və bazanı commit edirik
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
