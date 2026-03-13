"""

Bu kod parçası, FastAPI framework istifdə edilərək düzəldilmiş bir API router'ni təmsil edir. Bu router, istifadəçilərlə əlaqəli prosesləri idarə etmək üçün istifadə edilir. Hələlik iki ana endpoint daxil edilir: biri istifadəçi məlumatlarını almaq üçün, digəri isə istifadəçi şifrəsini dəyişdirmək üçün."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette import status

from dependencies import db_dependency, user_dependency, bcrypt_context
from models import Users

router = APIRouter(
    prefix='/user',
    tags=['👤 user']
)


class UserVerificationResponse(BaseModel):
    """
    Bu model, istifadəçinin cari şifrəsini və yeni şifrəsini ehtiva edən bir Pydantic modelidir.
     :param password: Bu model, istifadəçinin şifrə dəyişdirmə əməliyyatı üçün lazım olan məlumatları doğrulamaq və təmin etmək üçün istifadə olunur. "password" sahəsi, istifadəçinin cari şifrəsini təmsil edir və "new_password sahəsi isə istifadəçinin yeni şifrəsini təmsil edir.
     :param new_password: "new_password" sahəsi minimum 6 simvol uzunluğunda olmalıdır."""
    password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db: db_dependency):
    """
    Bu endpoint, cari istifadəçi məlumatlarını əldə etmək üçün istifadə olunur. İstifadəçi doğrulaması tələb olunur və yalnız autentifikasiya olunmuş istifadəçilər bu endpointə daxil ola bilərlər. Endpoint, verilənlər bazasından cari istifadəçinin məlumatlarını çəkir və onları JSON formatında geri qaytarır.
    :param user:
    :param db:
    :return:
    """
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    return db.query(Users).filter(Users.id == user.id).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency,
                    db: db_dependency,
                    user_verification: UserVerificationResponse):
    """
    Bu endpoint, istifadəçinin şifrəsini dəyişdirmək üçün istifadə olunur. İstifadəçi doğrulaması tələb olunur və yalnız autentifikasiya olunmuş istifadəçilər bu endpointə daxil ola bilərlər. Endpoint, istifadəçinin cari şifrəsini və yeni şifrəsini qəbul edir, cari şifrəni doğrulayır və əgər doğrulama uğurlu olarsa, yeni şifrəni verilənlər bazasında güncəlləyir.
    :param user_verification:
    :param user:
    :param db:
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.id).first()

    if not bcrypt_context.verify(user_verification.password, str(user_model.hashed_password)):
        raise HTTPException(status_code=401,
                            detail="Error on password change: Incorrect current password")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
