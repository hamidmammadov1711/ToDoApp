"""This module defines special endpoints for users with the "admin" role using FastAPI."""

from fastapi import APIRouter, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse

from dependencies import (
    db_dependency, user_dependency,
    get_current_user_from_cookie, get_translations_from_cookie
)
from models import Todos

router = APIRouter(
    prefix='/admin',
    tags=['🐱‍👤 admin']
)

templates = Jinja2Templates(directory="templates")

def redirect_to_login():
    """Redirect to the login page."""
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

@router.get("/admin-page")
async def render_admin_page(request: Request, db: db_dependency):
    """Renders the admin dashboard page."""
    user = await get_current_user_from_cookie(request)
    if user is None or user.get('user_role') != 'admin':
        return redirect_to_login()
    
    todos = db.query(Todos).all()
    t = get_translations_from_cookie(request)
    lang = request.cookies.get("lang", "az")
    return templates.TemplateResponse(request, "admin.html", {"todos": todos, "user": user, "t": t, "lang": lang})


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
