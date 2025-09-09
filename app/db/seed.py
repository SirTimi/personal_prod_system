from app.db.session import engine, Session, init_db
from app.db.models import User, Task
from datetime import datetime, timedelta

def seed():
    init_db()

    with Session(engine) as session:
        # Check if user already exists
        existing = session.query(User).filter(User.telegram_chat_id == 123456789).first()
        if existing:
            print("Seed data already exists.")
            return

        # Create fake user
        user = User(telegram_chat_id=123456789, tz="Africa/Lagos")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Add sample tasks
        tasks = [
            Task(user_id=user.id, title="Finish AI automation roadmap", priority="P1",
                 due_at=datetime.utcnow() + timedelta(hours=6)),
            Task(user_id=user.id, title="Read 10 pages of a book", priority="P2",
                 due_at=datetime.utcnow() + timedelta(days=1)),
        ]
        session.add_all(tasks)
        session.commit()

        print("Seed data inserted.")

if __name__ == "__main__":
    seed()
