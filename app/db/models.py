from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from sqlalchemy import Column, BigInteger

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_chat_id: int = Field(sa_column=Column(BigInteger, index=True, unique=True))
    tz: str = "Africa/Lagos"
    morning_hour: int = 6
    reflection_hour: int = 21
    weekly_hour: int = 7
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: list["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    reflections: list["Reflection"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # per-user foreign key
    user_id: int = Field(foreign_key="user.id")

    # per-user task number (starts from 1 for each user)
    task_number: int = Field(index=True)

    title: str
    description: Optional[str] = None
    status: str = "pending"   # pending | done | archived
    priority: str = "P2"
    due_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    user: User = Relationship(back_populates="tasks")

    __table_args__ = (
        UniqueConstraint("user_id", "task_number", name="uq_user_task_number"),
    )


class Reflection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: date
    shipped: Optional[str] = None
    blockers: Optional[str] = None
    tomorrow_one_thing: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="reflections")

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_user_reflection_date"),
    )
