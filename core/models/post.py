from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from typing import TYPE_CHECKING
#чтобы избежать ошибок с циклическими импортами
#проверим, что если сейчас идет только проверка типов
#без выполнения кода, тогда делаем импорт

if TYPE_CHECKING:
    from .user import User


class Post(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    
    #добавим внешний ключ
    #users название таблицы, id колонка на которую ссылаемся
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        
        )
    #тут в back_populates указывается поле в таблице юзера, с которого мы попадем 
    #в таблицу постов
    
    user: Mapped["User"] = relationship(back_populates="posts")