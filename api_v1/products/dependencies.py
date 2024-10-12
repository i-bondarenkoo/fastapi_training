from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Product

from . import crud

async def product_by_id(
    #эта функция получает текущий продукт ид и сессию
    #и возвращает нам продукт
    #сделано в виде зависимости depends
    #чтобы лишний раз самим не вызывать эту функцию
    product_id: Annotated[int, Path], 
    
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> Product:
    product =  await crud.get_product(
    session=session,
    product_id=product_id,
    )
    if product is not None:
        return product
    
    #Если объекта нет, выведем ошибку
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
