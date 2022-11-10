import sqlite3


def connect_db(app):
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db(app):
    """Вспомогательная функция для создания бд"""
    db = connect_db(app)
    with app.open_resource("sql_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FlaskDatabase:

    def __init__(self, db, table):
        self.__db = db
        self.__cur = db.cursor()
        self.table = table

    def add_menu(self, title, url):
        try:
            self.__cur.execute(f"INSERT INTO {self.table} VALUES (NULL, ?, ?)", (title, url))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
            return False
        return True

    def delete(self, id):
        try:
            self.__cur.execute(f"DELETE from {self.table} where id = {id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
            return False
        return True

    def add_list(self, _list):
        print(_list)
        for i in _list:
            print(i)
            if not self.add_menu(*i):
                return False
        return True
