from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings

from asyncio import current_task

#класс помощик для взаимодействия с БД
class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        #создаем движок для подключения
        self.engine =create_async_engine(
            url=url,
            echo=echo,
        )
        #session_factory фабрика сессий для работы с БД
        #sessionmaker будет создавать эти сессии
        #у него в качестве параметра bind=engine
        #создается фабрика сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            #autoflush=False — отключает автоматическую отправку изменений в базу перед запросами
            autoflush=False,
            #autocommit=False — требует явного вызова коммита для сохранения изменений.
            autocommit=False,
            #expire_on_commit=False — не удаляет объекты из сессии после коммита, что позволяет продолжать работать с ними
            expire_on_commit=False,
        )

    #Создает "скоупированную" (ограниченную) сессию с помощью async_scoped_session,
    # что позволяет привязывать сессию к текущей асинхронной задаче (current_task).
    # Это полезно в асинхронных приложениях, чтобы избежать пересечения сессий между задачами
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session
    
    #объект через который мы будем работать с 
    #асинхронной БД
    #get_scoped_session (выше) мы используем чтобы создавать сессию подключение к базе данных во время запросов
    #затем мы будем получать эту сессию внутри views функции (смотреть файл views)
    #Функция, реализующая асинхронный контекстный менеджер для работы с сессиями.
    # Используется async with для создания и закрытия сессии.
    # yield session возвращает текущую сессию для использования в запросах к БД, а затем закрывает её после завершения использования.
    async def session_dependency(self) -> AsyncSession:
        
        async with self.session_factory() as session:
            yield session
            await session.close()

    #Аналогичен session_dependency, но создает сессию через get_scoped_session.
    # В отличие от session_dependency, здесь используется "скоупированная" сессия
    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()        


#создадим экземпляр класса для удобства работы в дальнейшем
db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)        