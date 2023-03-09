from flask import g, Flask, render_template, redirect, url_for, request, session, abort, flash, make_response
from config import Config
import os
from database import FlaskDatabase, connect_db
import git

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


@app.route("/test")
def test():
    content = render_template("index.html", session=session, menu=menu)
    res = make_response(content)
    res.headers["Content-Type"] = "multipad/from data"
    res.headers["Server"] = "CUB Flask"
    return res


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
    db = FlaskDatabase(get_db())
    if "user_logged" not in session or session["user_logged"] != user:
        abort(401)
    return render_template("profile.html", menu=db.mainmenu, user=user)


@app.route("/post/<alias>")
def show_post(alias):
    db = FlaskDatabase(get_db())
    title, post = db.get_post(alias)
    return render_template("post.html", menu=db.mainmenu, post=post)


@app.route('/')
def main():
    return render_template("index.html", session=session, menu=menu)


@app.route("/update_server", methods=["POST"])
def webhook():
    if request.method == "POST":
        repo = git.Repo("/home/Boyarishnik2/Flask")
        origin = repo.remotes.origin
        origin.pull()
        return "update", 200
    else:
        return "Неправильный тип запроса", 400


# @app.route('/<name>/')
# def hello(name):
#     return f"<h1>Привет, {name}, ваш номер - {randint(1, 100)}</h1>"


@app.route('/Здарова/')
def index():

    return render_template("index1.html", menu=menu)


@app.route("/asdasdasd/")
def asd():
    return "Just a test"


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


# class Vertex:
#     ID = 0
#
#     def __init__(self):
#         self.links = list()
#         self.id = self.__class__.ID
#         self.__class__.ID += 1
#
#     def __repr__(self):
#         return f"---{self.id}"
#
#
# class Link:
#
#     def __init__(self, v1, v2):
#         self.v1 = v1
#         self.v2 = v2
#         v1.links.append(self)
#         v2.links.append(self)
#         self.dist = 1
#
#     def __repr__(self):
#         return f"{self.v1}{self.v2}---"
#
#
# def find_way(v1, v2):
#     return find(v1, v2, list(), 0, [v1])
#
#
# def find(v1, v2, lst, length, path):
#     if v1 == v2:
#         return length, path + [v1]
#
#     res = list()
#
#     for link in v1.links:
#
#         if link.v1 == v1 and link.v2 not in lst:
#             res.append(find(link.v2, v2, lst + [link.v1], length + link.dist, path))
#
#         if link.v2 == v1 and link.v1 not in lst:
#             res.append(find(link.v1, v2, lst + [link.v2], length + link.dist, path))
#
#     res = list(filter(lambda a: a is not None, res))
#     print(list(res))
#
#     if res:
#         return min(res, key=lambda a: a[0])