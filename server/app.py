from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
  return render_template('pages/home.html')

@app.route('/feature1')
def feature():
  return render_template("pages/feature1.html")