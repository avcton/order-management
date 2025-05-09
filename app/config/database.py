from sqlalchemy import create_engine
from app.config.settings import settings
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URI = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db_session():
    """Simplest possible session context manager"""
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
