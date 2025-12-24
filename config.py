import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    DB_USER = os.getenv('DB_USER', 'alebrotto')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'BrottoK@was0975')
    DB_HOST = os.getenv('DB_HOST', 'utils_postgress')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'utils')
    DB_SCHEMA = os.getenv('DB_SCHEMA', 'public')
    DB_TABLE = os.getenv('DB_TABLE', 'megasena')

    # Application Configuration
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
