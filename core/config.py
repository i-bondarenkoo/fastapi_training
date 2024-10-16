from pydantic_settings import BaseSettings
from pydantic import BaseModel

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    #путь к файлу с базой данных
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    # echo: bool = True
    echo: bool = False
    
    
class Settings(BaseSettings):
    #укажем префикс для api v1
    api_v1_prefix: str = "/api/v1"
    
    db: DbSettings = DbSettings()

#Проинициализируем настройки
# создадим экземпляр класса settings
# который будем использовать дальше в проекте
settings = Settings()    
