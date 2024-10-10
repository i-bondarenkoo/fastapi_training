from users.schemas import CreateUser


#функция принимает на вход класс-схему объявленную в schemas
#параметр называется user_in
def create_user(user_in: CreateUser) -> dict:
    # метод model_dump преобразует данные (атрибуты модели) в словарик
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }