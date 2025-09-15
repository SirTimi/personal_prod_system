from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Import models so SQLModel is aware of them
from app.db import models  

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
def reset_db():
    """Drop and recreate all tables"""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
