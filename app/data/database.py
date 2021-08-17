from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

from app.core.config import settings

uri = settings.DATABASE_URL

engine = create_engine(uri, echo=settings.DEVELOPMENT)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
mapper_registry = registry()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore
