from flask import g, Flask, render_template, redirect, url_for, request, session, abort
from time import sleep
from config import Config
import os
import database as db

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "flask.db")))

menu_list = [("Главная", '/'),
             ("Приветствие", '/Дмитрий'),
             ("index", '/index'),
             ("Здарова", "/Здарова"),
             ("Регистрация", "/signup"),
             ("Вход", "/signin"),
             ("DataBase", "/index_db")]

menu = db.FlaskDatabase(db.connect_db(app), "mainmenu")
menu.add_list(menu_list)

users = [{"name": "Dmitriy", "password": "123456789"},
         {"name": "Admin", "password": "Admin"}]


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = db.connect_db(app)
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()
@app.route("/profile/<user>")
def profile(user):
    if "user_logged" not in session or session["user_logged"] != user:
        abort(401)
    return user + f"<br><a href={url_for('exit')}>Выйти</a>"

@app.route('/')
def main():
    return render_template("index.html", id=2, menu=menu)

# @app.route('/<name>/')
# def hello(name):
#     return f"<h1>Привет, {name}, ваш номер - {randint(1, 100)}</h1>"

@app.route('/Здарова/')
def index():
    return render_template("index1.html", menu=menu)

@app.route("/index")
def indexx():
    i = 0
    while True:
        i += 1
        yield f"""<font size={i}>{i}</font>"""
        sleep(1)


@app.route("/signin", methods=["POST", "GET"])
def sign_in():
    print(request.method)
    if request.method == "POST":
        print(request.form["username"], request.form["password"])
    if "user_logged" in session:
        return redirect(url_for("profile", user=session["user_logged"]))
    elif request.method == "POST":
        for user in users:
            if request.form["username"] == user["name"] and request.form["password"] == user["password"]:
                session["user_logged"] = request.form["username"]
        return redirect(url_for("profile", user=session["user_logged"]))
    return render_template("signin.html")


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    print(list(map(lambda a: a["name"], users)))
    if request.method == "POST" and request.form["username"] not in map(lambda a: a["name"], users):
        users.append({"name": request.form["username"], "password": request.form["password"]})
        return redirect(url_for("sign_in"))
    return render_template("signup.html")


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


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
#hiiiii