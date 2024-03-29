import re
import sqlite3
from math import floor
from time import time

from flask import url_for


class TableDescr:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.get_table(self.name)

    def __set__(self, instance, value):
        instance.add_in_table(self.name, *value)


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
    users = TableDescr()
    mainmenu = TableDescr()
    posts = TableDescr()
    news = TableDescr()

    def add_in_table(self, table, *args):
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

    def get_table(self, table):
        try:
            sql = f"""SELECT * FROM {table}"""
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
        except sqlite3.Error as e:
            print(f"error {e}")
            return False
        return res

    def get_post(self, url):
        try:
            self.__cur.execute(f"SELECT * from posts where url = ?", (url,))
            res = self.__cur.fetchone()
            self.__db.commit()
            # text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
            #               "\\g<tag>"+base+"/\\g<url>>", res["text"])
            text = res['text']
        except sqlite3.Error as e:
            print(f"error {e}")
            return False
        return res["title"], text

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
            if not self.add_in_table("mainmenu", *i):
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
            self.add_in_table("posts", title, post, url, "Boyarishnik", tm)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД:", e)
            return False
        return True

    def del_table(self, table):
        self.__cur.execute(f"DROP TABLE {table}")

    def del_post(self, id):
        try:
            self.__cur.execute(f"DELETE from posts where id = {id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"error {e}")
            return False
        return True


if __name__ == "__main__":
    from app import app
    db = FlaskDatabase(connect_db(app))
    a = db.get_post("oymyakon")[1].replace("./", "/static/image")
    db.del_post(10)
    db.add_post(
        "oymyakon",
        a,
        "oymyakon"
    )
