from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


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