# файлик для выполнения запросов 

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post
from sqlalchemy import select
from sqlalchemy.engine import Result
#selectinload лучше использовать для связей ко многим
#joinedload чаще всего используют для подгрузки данных к одному
#selectinload чаще используют для подгрузки ко многим
from sqlalchemy.orm import joinedload, selectinload
#создаем пользователя
async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user

#ищем пользователя по имени
async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # #scalar_one_or_none выведет пользователя или ничего
    # #scalar_one выведет пользователя, если его не будет
    # #можно сделать исключение
    # user: User | None = result.scalar_one()
    #другой вариант
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user

#создадим фукнцию которая будет добавлять профиль для пользователя  
async def create_user_profile(
    session: AsyncSession, 
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    ) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile
    

#просмотр пользователей с профилем 
#joinedload будет подгружать данные, потому что в asyncio это важно
#с ним в одном запросе будет выбираться и юзер и профиль
async def show_users_with_profiles(session: AsyncSession,):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)
    
    
 #создадим новые посты для пользователя   
async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in posts_titles
        ]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts
  
#выведем пользователей и их посты  
async def get_users_with_posts(
    session: AsyncSession,
):
    #options нуже для подгрузки постов у юзера, в asyncio это важно, иначе будет ошибка
    #присоединили посты ко всем пользователям joinedload(User.posts)
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(
        # joinedload(User.posts),
        #selectinload делает отдельный запрос и подгружает все посты, отдельно пользователи не запрашиваются
        selectinload(User.posts),
        ).order_by(User.id)
    users = await session.scalars(stmt)
    #ниже 2 строчки делаются с 
    #for user in users
    # result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    #для случая selectinload unique не нужно использовать
    # users = result.scalars()
    #выводим всех по 1
    for user in users:
    # for user in users.unique(): # type: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)
            
            
#Загрузим   посты с авторами
async def get_posts_with_authors(session: AsyncSession):
    #joinedload(Post.user) загружаем юзеров для постов
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    #выведем посты и пользователей
    for post in posts:
        print("post", post)
        print("author", post.user)
    
#загрузим пользователей с постами и профилями
async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    
    for user in users:
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)
    
#функция с вложенными joins  
#запрос с профиля на юзера и с юзера на посты
async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        # .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        # .where(User.username == "bob")
        .order_by(Profile.id)
    )
    
    profiles = await session.scalars(stmt)
    
    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)
        
        
async def main():
    #контекстный менеджер для получения сессии и выполнения запросов (stmt)
    async with db_helper.session_factory() as session:
        # #создаем 2 пользователей в таблице юзерс (1)
        # # await create_user(session=session, username="john")
        # # await create_user(session=session, username="bob")
        # #Будем искать пользователя по имени (2)
        # user_john = await get_user_by_username(session=session, username="john")
        # # user_sam = await get_user_by_username(session=session, username="sam")
        # user_bob = await get_user_by_username(session=session, username="bob")
        # #создаем профили для пользователей (3)
        # await create_user_profile(
        #     session=session,
        #     user_id=user_john.id,
        #     first_name="John",
            
        #     )
        # #еще 1 профиль
        # await create_user_profile(
        #     session=session,
        #     user_id=user_bob.id,
        #     first_name="Bob",
        #     last_name="White",
        #     )
        #посмотрим профили пользователей (4)
        # await show_users_with_profiles(session=session)
        #создадим посты для пользователей (5)
        # user_john = await get_user_by_username(session=session, username="john")
        # user_bob = await get_user_by_username(session=session, username="bob")
        # user_andy = await get_user_by_username(session=session, username="andy")
        # await create_posts(
        #     session,
        #     user_john.id,
        #     "SQLA 2.0",
        #     "SqlA Joins",
        #     )
        # await create_posts(
        #     session,
        #     user_bob.id,
        #     "FastAPI intro",
        #     "FastAPI Advanced",
        #     "FastAPI more",
        # )
        #выведем пользователей с постами (6)
        # await get_users_with_posts(session=session)
        #выведем посты с авторами (7)
        # await get_posts_with_authors(session=session)
        #загрузим пользователей с постами и профилями (8)
        # await get_users_with_posts_and_profiles(session=session)
        #функция запрос с вложенными joins (9)
        await get_profiles_with_users_and_users_with_posts(session=session)
        
        
if __name__ == '__main__':
    asyncio.run(main())