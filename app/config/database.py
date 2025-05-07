from sqlalchemy import create_engine
from app.config.settings import settings
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URI = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
