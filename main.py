from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.models import Base, db_helper

from core.config import settings

import uvicorn

from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1


#Создаем таблицы вместе с запуском приложения
# до yield то что нам нужно для старта приложения
#после yield уборка, удаление не нухжных данных
@asynccontextmanager
async def lifespan(app: FastAPI):
    #создание всех таблиц в приложении
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)




@app.get("/")
def hello_index():
    return {
        "message": "hello index!",
    }
    



#name параметр запроса с значением по умолчанию
@app.get("/hello/")
def hello(name: str = "World"):
    #strip убирает лишние пробелы слева и справа
    name = name.strip().title()
    return {"message": f"Hello, {name}!"}
    



@app.get("/calc/add/")
def add( a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }
    
    

    
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)