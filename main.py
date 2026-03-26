""" FastAPI layihəsi üçün main (əsas) tətbiq faylı. Bu fayl FastAPI tətbiqini işə salır, verilənlər bazasını qurur və identifikasiya və todo idarəetməsi üçün marşrutlaşdırıcıları ehtiva edir. Lazımi modulları idxal edir, müəyyən edilmiş modellərə əsasən verilənlər bazası cədvəllərini yaradır və istifadəçi identifikasiyası və todo əməliyyatları ilə əlaqəli API sorğularını idarə etmək üçün identifikasiya və todo marşrutlaşdırıcılarını ehtiva edir. """

from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter
import time
from logger import logger

from database import engine
from models import Base
from routers import auth, todos, admin, users
from dependencies import get_translations_from_cookie

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
templates = Jinja2Templates(directory="templates")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.client.host if request.client else '127.0.0.1'} - \"{request.method} {request.url.path}\" {response.status_code} ({process_time:.4f}s)")
    return response

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        t = get_translations_from_cookie(request)
        lang = request.cookies.get("lang", "az")
        return templates.TemplateResponse(request, "404.html", {"t": t, "lang": lang}, status_code=404)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/set-language/{lang}")
def set_language(lang: str, request: Request):
    # Dili dəyişmək üçün cookie təyin edib əvvəlki səhifəyə qaytarır
    referer = request.headers.get("referer") or "/"
    response = RedirectResponse(url=referer, status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="lang", value=lang, httponly=False, max_age=31536000)
    return response

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
