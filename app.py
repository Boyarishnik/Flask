from flask import Flask, render_template
from random import randint
from time import sleep


app = Flask(__name__)
menu = [{"name": "Главная", "url": '/'},
        {"name": "Приветствие", "url": '/Дмитрий/'},
        {"name": "id", "url": '/123/'},
        {"name": "index", "url": '/index/'}]

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
        yield str(i)
        sleep(1)

if __name__ == "__main__":
    app.run(debug=True)
#hiiiii