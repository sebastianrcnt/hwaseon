import json
from flask import Flask, render_template
from legacy.blog_rank_new import get_blog_data

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


@app.route("/feature4")
def feature4():  # 대량키워드 요약
    return render_template('pages/feature4.html')


@app.route("/feature5")
def feature5():  # 대량키워드 요약
    return render_template('pages/feature5.html')

# API Routes


@app.route("/api/blog_rank")
def get_blog_rank():
    data = get_blog_data('woojung357')
    return json.dumps(data)
