from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UserRelationMixin
from typing import TYPE_CHECKING
#чтобы избежать ошибок с циклическими импортами
#проверим, что если сейчас идет только проверка типов
#без выполнения кода, тогда делаем импорт

if TYPE_CHECKING:
    from .user import User


class Post(UserRelationMixin, Base):
    
    # _user_id_nullable = False
    # _user_id_unique = False
    _user_back_populates = "posts"
    
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    
    #это все не нужно, после добавления отдельного класса UserRelationMixin
    # #добавим внешний ключ
    # #users название таблицы, id колонка на которую ссылаемся
    # user_id: Mapped[int] = mapped_column(
    #     ForeignKey("users.id"),
        
    #     )
    # #тут в back_populates указывается поле в таблице юзера, с которого мы попадем 
    # #в таблицу постов
    
    # user: Mapped["User"] = relationship(back_populates="posts")
    
    
    #для того чтобы было красивое строковое представление пользователя и данных
    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id}, username={self.title!r}, user_id={self.user_id})"
    
    
    #красивое представление в виде списка
    def __repr__(self):
        return str(self)