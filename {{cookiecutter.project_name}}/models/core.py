from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

class DB_Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = DB_Settings()

engine_url = URL.create(
    drivername="psycopg2+postgresql",
    username=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    database=settings.DB_NAME
)
engine = create_engine(engine_url)
local_session = sessionmaker(bind=engine)

def get_db_session():
    sess = local_session()
    try:
        yield sess
    finally:
        sess.close()
