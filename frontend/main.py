from flask import Flask, request, jsonify, url_for, render_template
from flask import redirect, url_for
import time

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<name>")
def greet(name):
    return render_template("index.html", name=name)


@app.route("/admin/")
def admin():
    time.sleep(5)  # Countdown for 5 seconds
    return redirect(url_for("home"))


@app.route("/get-user/<user_id>")
def get_user(user_id):

    user_data = {"user_id": user_id, "name": "John Doe", "email": "johndoe@example.com"}

    extra = request.args.get("extra")

    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200


@app.route("/create-user", methods=["POST"])
def create_user():

    if request.method == "POST":
        data = request.get_json()

        return jsonify(data), 201


if __name__ == "__main__":
    app.run(debug=True)
