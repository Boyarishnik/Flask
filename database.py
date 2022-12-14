import sqlite3
from math import floor
from time import time


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

    def __add_in_table(self, table, *args):
        try:
            print(f"INSERT INTO {table} VALUES (NULL, {('?, ' * (len(args) - 1)) + '?'})", len(args))
            print(args)
            self.__cur.execute(f"INSERT INTO {table} VALUES (NULL, {('?, ' * (len(args) - 1)) + '?'})", args)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
            return False
        return True

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def add_menu(self, title, url):
        # try:
        #     self.__cur.execute(f"INSERT INTO {self.title} VALUES (NULL, ?, ?)", (title, url))
        #     self.__db.commit()
        # except sqlite3.Error as e:
        #     print(f"error {e}")
        #     return False
        # return True
        self.__add_in_table("mainmenu", title, url)

    def __get_table(self, table):
        try:
            sql = f"""SELECT * FROM {table}"""
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print(f"error {e}")
            return False
        return res

    def get_menu(self):
        return self.__get_table("mainmenu")

    def get_users(self):
        return self.__get_table("users")

    def delete(self, id):
        try:
            self.__cur.execute(f"DELETE from mainmenu where id = {id}")
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

    def add_post(self, title, post, url):
        try:
            if self.__cur.execute("SELECT COUNT() as 'count' FROM posts WHERE url LIKE ?", (url,)):
                res = self.__cur.fetchone()
                if res["count"] > 0:
                    print("Статья с таким url уже существует")
                    return False
            tm = floor(time())
            self.__add_in_table("posts", title, post, url, "Boyarishnik", tm)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД:", e)
            return False
        return True

    def add_user(self, name, password):
        self.__add_in_table("users", name, password)


if __name__ == "__main__":
    from app import app
    db = FlaskDatabase(connect_db(app))
