#абсолютный импорт users.schemas
from users.schemas import CreateUser
# относительный импорт .schemas
#from .schemas import CreateUser
from fastapi import APIRouter

from users import crud


router = APIRouter(prefix="/users", tags=["Users"])

#параметр тела запроса
@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
        #передаем наш объект user из crud
        #     user = user_in.model_dump()
        # return {
        #     "success": True,
        #     "user": user,
        # }
        
    


