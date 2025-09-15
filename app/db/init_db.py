from app.db.session import reset_db, engine
from sqlmodel import SQLModel
from app.db import models

def init_db():
    SQLModel.metadata.create_all(engine)

