from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dd")
def dd():
    return render_template("dependent_dropdown.html")

@app.route("/crud")
def crud():
    return render_template("crud.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
