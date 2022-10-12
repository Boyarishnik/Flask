from flask import Flask, render_template, redirect, url_for
from random import randint
from time import sleep


app = Flask(__name__)
app.config["SECRET_KEY"] = 'asdasd'
menu = [{"name": "Главная", "url": '/'},
        {"name": "Приветствие", "url": '/Дмитрий/'},
        {"name": "index", "url": '/index/'},
        {"name": "Здарова", "url": "/Здарова/"},
        {"name": "Регистрация", "url": "/sign_in/"}]

@app.route('/')
def main():
    return render_template("index.html", id=2, menu=menu)

@app.route('/<name>/')
def hello(name):
    return f"<h1>Привет, {name}, ваш номер - {randint(1, 100)}</h1>"

@app.route('/Здарова/')
def index():
    return render_template("index1.html", menu=menu)

@app.route("/index/")
def indexx():
    i = 0
    while True:
        i += 1
        yield f"""<font size={i}>{i}</font>"""
        sleep(1)

@app.route("/sign_in/")
def signing():
    return render_template("signing.html", title=menu)

@app.route("/sign_in/", methods=["POST", "GET"])
def sign_in():
    if "user_logged" in session:
        return redirect(url_for("profile", username=session["user_logged"]))
    elif request.form["username"] == "aaaa" and request.form["password"] == 12345:
        session["user_logged"] = request.form["username"]
        return redirect(url_for("profile", username=session["user_logged"]))
    return render_template("sign_in.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html", menu=menu), 404

if __name__ == "__main__":
    app.run(debug=True)
#hiiiii