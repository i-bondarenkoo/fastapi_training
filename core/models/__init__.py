#в all указываем объекты которые будем добавлять и использовать
#в других файлах
__all__ = (
    "Base",
    "Product",
    "db_helper",
    "DatabaseHelper",
)

#импорт чтобы другие папки и модули видели наши модели
from .base import Base
from .product import Product
from .db_helper import db_helper, DatabaseHelper