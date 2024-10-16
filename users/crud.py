from users.schemas import CreateUser


#функция принимает на вход класс-схему объявленную в schemas
#параметр называется user_in
#Когда вы вызываете функцию create_user, вы передаете ей объект CreateUser,
# содержащий данные пользователя (например, username и email).
# Параметр user_in становится этим объектом модели CreateUser
# и используется для доступа к данным, которые были переданы
def create_user(user_in: CreateUser) -> dict:
    # метод model_dump преобразует данные (атрибуты модели) в словарик
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }