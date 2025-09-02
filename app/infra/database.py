import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://developer:devbpassword@localhost:25000/developer")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)