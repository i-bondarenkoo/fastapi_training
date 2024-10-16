from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . post import Post
    from .profile import Profile

class User(Base):
    
    username: Mapped[str] = mapped_column(String(32), unique=True)
    
    #юзер ссылает на список  постов
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")