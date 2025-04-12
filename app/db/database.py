from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    print("Database engine created successfully.")
except Exception as e:
    print("Failed to create engine:", e)
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    from . import models  
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
except Exception as e:
    print("Failed to create tables:", e)
    raise


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()