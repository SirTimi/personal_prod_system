from app.db.session import reset_db

if __name__ == "__main__":
    print("🚀 Resetting & initializing database...")
    reset_db()
    print("✅ Database ready.")