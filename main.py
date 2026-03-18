""" FastAPI layihəsi üçün main (əsas) tətbiq faylı. Bu fayl FastAPI tətbiqini işə salır, verilənlər bazasını qurur və identifikasiya və todo idarəetməsi üçün marşrutlaşdırıcıları ehtiva edir. Lazımi modulları idxal edir, müəyyən edilmiş modellərə əsasən verilənlər bazası cədvəllərini yaradır və istifadəçi identifikasiyası və todo əməliyyatları ilə əlaqəli API sorğularını idarə etmək üçün identifikasiya və todo marşrutlaşdırıcılarını ehtiva edir. """

from fastapi import FastAPI

import models
from database import engine
from routers import auth, todos, admin, users

app = FastAPI(
    title="Todo API",
    description="Bu API, istifadəçilərin todo tapşırıqlarını idarə etmələrinə imkan verir. İstifadəçilər qeydiyyatdan keçə və daxil ola bilərlər, sonra isə öz todo tapşırıqlarını yarada, oxuya, yeniləyə və silə bilərlər. Hər bir istifadəçi yalnız öz tapşırıqlarını görə və idarə edə bilər.",
    version="1.0.1",
    
)

models.Base.metadata.create_all(bind=engine)

@app.get("/helathy")
def helathy():
    return {"message": "API is healthy and running!"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
