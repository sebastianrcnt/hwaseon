from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
  return render_template('pages/home.html')

@app.route("/keywords")
def get_keywords_page():
  return render_template("pages/keywords.html")