

#create, read, update, delete
#создание, чтение, обновление и удаление объектов
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from sqlalchemy import select
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial

#чтение и возврат всех товаров из базы
async def get_products(session: AsyncSession) -> list[Product]:
    #запрос всех товаров из базы
    #выражение stmt
    #order by сортируем по id
    stmt = select(Product).order_by(Product.id)
    #execute - выполнить выражение
    result: Result = await session.execute(stmt)
    #all превращает данные в список
    #scalars позволяет получить сразу все товары, а не tuple(кортеж)
    products = result.scalars().all()
    return list(products)


async def get_product( session: AsyncSession, product_id: int) -> Product | None:
    #возвращаем Product 
    # по какому id ?
    # по product_id
    return await session.get(Product, product_id)


async def create_product(session : AsyncSession, product_in: ProductCreate) -> Product:
    #так как из атрибутов нашей модели придет словарь
    #то с помощью ** распакуем словарь на kwargs
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(product)
    return product


#обновление данных
#put обновляет целиком
#patch обновляет данные частично

async def update_product(
        session: AsyncSession,
              product: Product, 
              product_update: ProductUpdate | ProductUpdatePartial,
              partial: bool = False,
            ) ->Product:
    #пробежимся в словаре по n, v name value
    #получим словарик model_dump
    # идем по всем элементам .items()
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()    
    return product



async def delete_product(
        session: AsyncSession,
        product: Product,

) -> None:
    await session.delete(product)
    await session.commit()
