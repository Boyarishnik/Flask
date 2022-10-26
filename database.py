import sqlite3
from app import app


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания бд"""
    db = connect_db()
    with app.open_resource("sql_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


create_db()
print(create_db.__doc__)