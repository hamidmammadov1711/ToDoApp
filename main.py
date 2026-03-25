""" FastAPI layihəsi üçün main (əsas) tətbiq faylı. Bu fayl FastAPI tətbiqini işə salır, verilənlər bazasını qurur və identifikasiya və todo idarəetməsi üçün marşrutlaşdırıcıları ehtiva edir. Lazımi modulları idxal edir, müəyyən edilmiş modellərə əsasən verilənlər bazası cədvəllərini yaradır və istifadəçi identifikasiyası və todo əməliyyatları ilə əlaqəli API sorğularını idarə etmək üçün identifikasiya və todo marşrutlaşdırıcılarını ehtiva edir. """

from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from database import engine
from models import Base
from routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    """

    :return:
    """
    return {'message': 'API is healthy and running!'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
