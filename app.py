from flask import Flask, render_template
from random import randint
app = Flask(__name__)


@app.route('/')
def main():
    return "<a href=\"/index/\">index1asd</a>"

#sdgsdgsdgфывфыв
@app.route('/<name>/')
def hello(name):
    return f"<h1>Привет, {name}, ваш номер - {randint(1, 100)}</h1>"

@app.route('/index/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
