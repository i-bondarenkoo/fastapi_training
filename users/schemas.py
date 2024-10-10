#BaseModel базовый класс для создания классов-моделей
from pydantic import BaseModel, EmailStr
from pydantic import Field

from typing import Annotated
from annotated_types import MaxLen, MinLen


class CreateUser(BaseModel):
    #... указывает что поле обязательно для заполнения
    username: str = Field(... , min_length=3, max_length=25)
    #username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
