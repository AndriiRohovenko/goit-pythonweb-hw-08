from src.db.configurations import session
from sqlalchemy import text, select, func
from sqlalchemy.orm import Session


def check_database_connection(session: Session) -> bool:
    try:
        with session:
            # Simple query to check the connection
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False


if __name__ == "__main__":

    with session:
        result1 = check_database_connection(session)
        print(result1)
