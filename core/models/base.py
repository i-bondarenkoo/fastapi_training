#файл с основой, тем что нам понадобится для
#работы в дальнейшем

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

class Base(DeclarativeBase):
    #это свойство указывает, что модель абстрактная 
    #она не будет создана в нашей базе данных
    #вместе с остальными таблицами
    __abstract__ = True

    @declared_attr.directive
    #за счет этой функции имя таблицы будет 
    #автоматически генерироваться в нижнем регистре
    #__name__.lower()
    #f строка нужна чтобы добавить к имени s(во множественном числе)
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    #в базовый класс(родительский)
    #от которого наследуются остальные классы/модели таблиц в бд
    #вынесем поле которое будет повторяться во многих таблицах
    id: Mapped[int] = mapped_column(primary_key=True)