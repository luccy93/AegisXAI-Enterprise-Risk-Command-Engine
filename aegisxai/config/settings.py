import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "aegisxai")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    SECRET_KEY = os.getenv("SECRET_KEY", "aegisxai-default-secret-key")
    MODEL_VERSION = os.getenv("MODEL_VERSION", "v4.0.0")
    CSV_PATH = os.getenv("CSV_PATH", "aegisxai/data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def get_db_url(cls):
        if cls.APP_ENV == "development":
            return "sqlite:///./aegisxai.db"
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
