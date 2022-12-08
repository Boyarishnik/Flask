from flask import g, Flask, render_template, redirect, url_for, request, session, abort
from time import sleep
from config import Config
import os
from database import FlaskDatabase, connect_db

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "flask.db")))

menu_list = [("Главная", '/'),
             ("Приветствие", '/Дмитрий'),
             ("Здарова", "/Здарова"),
             ("Регистрация", "/signup"),
             ("Вход", "/signin"),
             ("DataBase", "/db/index_db")]

menu = [{"name": i, "url": j} for i, j in menu_list]
# menu = db.FlaskDatabase(db.connect_db(app), "mainmenu")
# menu.add_list(menu_list)

users = [{"name": "Dmitriy", "password": "123456789"},
         {"name": "Admin", "password": "Admin"}]


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db(app)
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/db/index_db/")
def index_db():
    db = get_db()
    db = FlaskDatabase(db, "mainmenu")
    return render_template("index_db.html", menu=db.get_menu())


@app.route("/profile/<user>")
def profile(user):
    if "user_logged" not in session or session["user_logged"] != user:
        abort(401)
    return user + f"<br><a href={url_for('exit')}>Выйти</a>"


@app.route('/')
def main():
    return render_template("index.html", session=session, menu=menu)


# @app.route('/<name>/')
# def hello(name):
#     return f"<h1>Привет, {name}, ваш номер - {randint(1, 100)}</h1>"


@app.route('/Здарова/')
def index():

    return render_template("index1.html", menu=menu)


# @app.route("/index")
# def indexx():
#     i = 0
#     while True:
#         i += 1
#         yield f"""<font size={i}>{i}</font>"""
#         sleep(1)


@app.route("/signin", methods=["POST", "GET"])
def sign_in():
    db = FlaskDatabase(get_db(), "users")
    if "user_logged" in session:
        return redirect(url_for("profile", user=session["user_logged"]))
    elif request.method == "POST":
        for user in db.get_menu():
            if request.form["username"] == user["username"] and str(request.form["password"]) == user["password"]:
                session["user_logged"] = request.form["username"]
                return redirect(url_for("main"))
    return render_template("signin.html", menu=menu)


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    db = FlaskDatabase(get_db(), "users")
    print(list(map(lambda a: a["name"], users)))
    if request.method == "POST" and request.form["username"] not in map(lambda a: a["name"], users):
        db.add_menu(request.form["username"], request.form["password"])
        return redirect(url_for("sign_in"))
    return render_template("signup.html", menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html", menu=menu), 404


@app.errorhandler(401)
def error(error):
    return "<h1>Некорректное значение</h1>"


@app.route("/exit")
def exit():
    del session["user_logged"]
    return redirect(url_for("sign_in"))

@app.route("/asd/")
def add():
    db = FlaskDatabase(get_db(), "mainmenu")
    return render_template("add.html", menu=db.get_menu())


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
# hiiiii
