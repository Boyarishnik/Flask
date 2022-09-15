from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return "<a href=\"/index/\">index1asd</a>"

#sdgsdgsdgфывфыв
@app.route('/index/')
def hello():
    return render_template("index.html",
                           user={"username": "user"})


if __name__ == "__main__":
    app.run(debug=True)
