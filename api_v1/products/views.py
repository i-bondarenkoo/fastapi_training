from fastapi import APIRouter
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial

from . dependencies import product_by_id
from core.models import db_helper
from fastapi import HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Products"])

@router.get("/", response_model=list[Product])
#дб хелпер автоматически вызовет session_dependency (саму сессию)
#а потом автоматически закроет эту сессию
async def get_products(
    #затем мы будем получать эту сессию внутри views функции (смотреть файл views)
    session:AsyncSession = Depends(db_helper.scoped_session_dependency),
    ):
    return await crud.get_products(
        session=session,
        )

@router.post("/", 
        response_model=Product, 
        status_code=status.HTTP_201_CREATED,
        )
async def create_product(

    #так же получаем помимо сессии, дополнительные данные
    #из тела ( тело запроса)
    product_in: ProductCreate,
    #затем мы будем получать эту сессию внутри views функции (смотреть файл views)
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ):
    #внутри этой функции мы выполняем действия описанные 
    # в файле product/crud (папка products файл crud)
    return await crud.create_product(
        session=session,
        product_in=product_in,
        )


#эта функция только переписанная проще ниже
# @router.get("/{product_id}/", response_model=Product)
# async def get_product(
#     #так же получаем помимо сессии, дополнительные данные
#     #из {product_id} параметр пути
#     product_id: int, 
#     #затем мы будем получать эту сессию внутри views функции (смотреть файл views)
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency)
#     ):
#     product =  await crud.get_product(
#         session=session,
#         product_id=product_id,
#         )
#     if product is not None:
#         return product
    
#     #Если объекта нет, выведем ошибку
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Product {product_id} not found!",
#     )


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product: Product = Depends(product_by_id),
):
    return product


@router.put("/{product_id}/")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )
    


@router.patch("/{product_id}/")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )
        

        
@router.delete("/{product_id}/",
     status_code=status.HTTP_204_NO_CONTENT,)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(
        session=session,
        product=product,
    )