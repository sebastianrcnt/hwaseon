from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('pages/home.html')


@app.route('/feature1')
def feature1():
    return render_template("pages/feature1.html")


@app.route('/feature2')
def feature2():  # coupang
    return render_template("pages/feature2.html")


@app.route('/feature3')
def feature3():  # naver
    return render_template('pages/feature3.html')


@app.route("/feature4")
def feature4():  # 대량키워드 요약
    return render_template('pages/feature4.html')
