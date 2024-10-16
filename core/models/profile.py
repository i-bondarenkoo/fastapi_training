from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UserRelationMixin

# if TYPE_CHECKING:
#     from .user import User
    
    
class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"
    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))  
    bio: Mapped[str | None]
    
    
    #после создания UserRelationMixin нам это не нужно
    # #объявим ссылку на таблицу пользователя
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
