"""Bu kod parçacığı, FastAPI istifadə edərək bir "Todo" tətbiqinin API marşrutlarını təyin edir.
CRUD (Yarat, Oxu, Yenilə, Sil) əməliyyatlarını həyata keçirir."""

from fastapi import APIRouter, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import RedirectResponse

from dependencies import (
    db_dependency, user_dependency,
    get_current_user_from_cookie, get_translations_from_cookie
)
from models import Todos

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/todos',
    tags=['📄 todos']
)


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def redirect_to_login():
    """Login səhifəsinə yönləndirmə."""
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency, skip: int = 0, limit: int = 50):
    """Todo siyahısı səhifəsini render edir."""
    user = await get_current_user_from_cookie(request)
    if user is None:
        return redirect_to_login()

    todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).offset(skip).limit(limit).all()
    t = get_translations_from_cookie(request)
    lang = request.cookies.get("lang", "az")
    return templates.TemplateResponse(request, "todo.html", {"todos": todos, "user": user, "t": t, "lang": lang})


@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    """Yeni todo əlavə etmə səhifəsini render edir."""
    user = await get_current_user_from_cookie(request)
    if user is None:
        return redirect_to_login()
    t = get_translations_from_cookie(request)
    lang = request.cookies.get("lang", "az")
    return templates.TemplateResponse(request, "add-todo.html", {"user": user, "t": t, "lang": lang})


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    """Todo redaktə səhifəsini render edir."""
    user = await get_current_user_from_cookie(request)
    if user is None:
        return redirect_to_login()

    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    t = get_translations_from_cookie(request)
    lang = request.cookies.get("lang", "az")
    return templates.TemplateResponse(request, "edit-todo.html", {"todo": todo, "user": user, "t": t, "lang": lang})


### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency, skip: int = 0, limit: int = 50):
    """Bütün todoları qaytarır (səhifələmə ilə)."""
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).offset(skip).limit(limit).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    """Tək bir todonu qaytarır."""
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest):
    """Yeni todo yaradır."""
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    """Todonu yeniləyir."""
    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    """Todonu silir."""
    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()
