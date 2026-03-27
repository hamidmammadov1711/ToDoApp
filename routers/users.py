"""This piece of code is used to manage processes related to users.
Endpoints for retrieving user information, changing password, and updating phone number."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import RedirectResponse

from dependencies import (
    db_dependency, user_dependency, bcrypt_context,
    get_current_user_from_cookie, get_translations_from_cookie
)
from models import Users

router = APIRouter(
    prefix='/user',
    tags=['👤 user']
)

templates = Jinja2Templates(directory="templates")

def redirect_to_login():
    """Redirect to the login page."""
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

@router.get("/profile-page")
async def render_profile_page(request: Request, db: db_dependency):
    """Renders the user profile page."""
    user_cookie = await get_current_user_from_cookie(request)
    if user_cookie is None:
        return redirect_to_login()
    
    user_db = db.query(Users).filter(Users.id == user_cookie.get('id')).first()
    if user_db is None:
        return redirect_to_login()

    t = get_translations_from_cookie(request)
    lang = request.cookies.get("lang", "az")
    return templates.TemplateResponse(request, "profile.html", {"user": user_cookie, "user_db": user_db, "t": t, "lang": lang})


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    """Returns user data"""
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    """The user changes their password"""
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency,
                              phone_number: str):
    """Updating phone number"""
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
