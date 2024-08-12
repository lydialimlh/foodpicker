from flask import (
    Flask,
    flash,
    request,
    jsonify,
    url_for,
    render_template,
    session,
    redirect,
    url_for,
)
from datetime import timedelta
import time


app = Flask(__name__)
app.secret_key = "abc123"
app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/")
def home():

    if "user" in session:
        user = session["user"]
        flash(f"You are logged in as {user}!", "info")
    else:
        user = "Guest"
        flash(f"You are not logged in. Click on Login button above to login.", "info")
    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user  # super simple way to store user data as a dictionary
        flash(f"Login successful, {user}!", "info")

        return redirect(url_for("user", usr=user))

    else:
        if "user" in session:
            flash(f"Already logged in!", "info")
            return redirect(url_for("user", usr=session["user"]))

        return render_template("login.html")


@app.route("/user")
def user():

    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash(f"You are not logged in!", "info")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():

    flash(f"You have been logged out!", "info")

    session.pop("user", None)
    return redirect(url_for("login"))


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
