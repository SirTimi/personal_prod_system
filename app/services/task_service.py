from sqlmodel import select
from app.db.session import engine, Session
from app.db.models import Task

def get_tasks_for_user(user_id: int):
    with Session(engine) as session:
        return session.exec(
            select(Task).where(Task.user_id == user_id, Task.status == "pending")
        ).all()

def create_task(user_id: int, title: str, priority: int = 1):
    with Session(engine) as session:
        # Find last task_number for this user
        last_task = session.exec(
            select(Task).where(Task.user_id == user_id).order_by(Task.task_number.desc())
        ).first()
        next_number = (last_task.task_number + 1) if last_task else 1

        task = Task(
            user_id=user_id,
            task_number=next_number,
            title=title,
            priority=priority,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task