from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('pages/home.html')


@app.route('/feature1')
def feature1():
    return render_template("pages/feature1.html")


@app.route('/feature2')
def feature2():
    return render_template("pages/feature2.html")
