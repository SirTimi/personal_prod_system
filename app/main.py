from app.db.session import init_db

def main():
    print("Initializing database...")
    init_db()
    print("Database ready.")

if __name__ == "__main__":
    main()
