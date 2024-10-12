from pydantic_settings import BaseSettings


from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    #укажем префикс для api v1
    api_v1_prefix: str = "/api/v1"
    
    #путь к файлу с базой данных
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # db_echo: bool = True
    db_echo: bool = False


#Проинициализируем настройки
# создадим экземпляр класса settings
# который будем использовать дальше в проекте
settings = Settings()    
