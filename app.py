from flask import g, Flask, render_template, redirect, url_for, request, session, abort, flash
from config import Config
import os
from database import FlaskDatabase, connect_db
# import git

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


@app.route("/db/index_db/", methods=["POST", "GET"])
def index_db():
    db = get_db()
    db = FlaskDatabase(db)
    if request.method == "POST":
        db.del_post(request.form["id"])
        print(request.form["id"])
    return render_template("index_db.html", menu=db.mainmenu, posts=db.posts)


@app.route("/profile/<user>")
def profile(user):
    if "user_logged" not in session or session["user_logged"] != user:
        abort(401)
    return user + f"<br><a href={url_for('exit')}>Выйти</a>"


@app.route("/post/<alias>")
def show_post(alias):
    db = FlaskDatabase(get_db())
    title, post = db.get_post(alias)
    return render_template("post.html", menu=db.mainmenu, post=post)


@app.route('/')
def main():
    return render_template("index.html", session=session, menu=menu)

# @app.route("/update_server", method=["POST", "GET"])
# def webhook():
#     if request.method == "POST":
#         repo = git.Repo("/home/Boyarishnik2/Flask")
#         origin = repo.remotes.origin
#         origin.pull()
#         return "update", 200
#     else:
#         return "Неправильный тип запроса", 400


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
    db = FlaskDatabase(get_db())
    if "user_logged" in session:
        return redirect(url_for("profile", user=session["user_logged"]))
    elif request.method == "POST":
        for user in db.users:
            if request.form["username"] == user["username"] and str(request.form["password"]) == user["password"]:
                session["user_logged"] = request.form["username"]
                return redirect(url_for("main"))
    return render_template("signin.html", menu=menu)


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    db = FlaskDatabase(get_db())
    if request.method == "POST" and request.form["username"] not in map(lambda a: a["name"], users):
        db.user = (request.form["username"], request.form["password"])
        return redirect(url_for("sign_in"))
    return render_template("signup.html", menu=menu)


@app.route("/news/")
def news():
    db = FlaskDatabase(get_db())
    return render_template("news.html", menu=db.mainmenu, news=db.news)


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


@app.route("/asd/", methods=["POST", "GET"])
def add():
    db = FlaskDatabase(get_db())
    if request.method == "POST":
        if 40 > len(request.form["name"]) > 3 and 10 < len(request.form["post"]) < 2 ** 20:
            if not db.add_post(request.form["name"], request.form["post"], request.form["url"]):
                flash("ошибка добавления статьи", category="error")
            else:
                flash("статья успешно добавлена", category="success")
        else:
            flash("ошибка добавления статьи", category="error")
    return render_template("add.html", menu=db.mainmenu)


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)