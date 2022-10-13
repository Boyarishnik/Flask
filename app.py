from flask import Flask, render_template, redirect, url_for, request, session
from random import randint
from time import sleep


app = Flask(__name__)
app.config["SECRET_KEY"] = 'asdasdxfgdfhfjyid6kdr6jed6jdsr6kyut8'
menu = [{"name": "Главная", "url": '/'},
        {"name": "Приветствие", "url": '/Дмитрий'},
        {"name": "index", "url": '/index'},
        {"name": "Здарова", "url": "/Здарова"},
        {"name": "Регистрация", "url": "/signin"}]

print(menu[1]["name"])
@app.route("/profile/<user>")
def profile(user):
    print(user)
    return user

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
    elif request.method == "POST" and request.form["username"] == "D" and request.form["password"] == "1":
        session["user_logged"] = request.form["username"]
        return redirect(url_for("profile", user=session["user_logged"]))
    return render_template("signin.html")

@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    pass

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html", menu=menu), 404

if __name__ == "__main__":
    app.run(debug=True)
#hiiiii