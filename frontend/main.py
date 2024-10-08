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
from flask_sqlalchemy import SQLAlchemy
import time


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "abc123"
app.permanent_session_lifetime = timedelta(minutes=1)


db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():

    if "user" in session:
        user = session["user"]
        flash(f"You are logged in as {user}!", "info")
    else:
        user = "Guest"
        flash(
            f"You are not logged in. Click on Login button above to login.",
            "info",
        )
    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user  # super simple way to store user data as a dictionary

        found_user = users.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash(f"Login successful, {user}!", "info")

        return redirect(url_for("user", usr=user))

    else:
        if "user" in session:

            flash(f"Already logged in!", "error")

            # return redirect(url_for("user", usr=session["user"]))
            return redirect(url_for("home"))

        return render_template("login.html")


@app.route("/delete-all", methods=["GET", "POST"])
def delete_all():
    if request.method == "GET":  # when the user lands on the page
        return render_template("delete-all.html")

    if request.method == "POST":
        users.query.delete()
        db.session.commit()
        session.pop("user", None)
        session.pop("email", None)
        flash(f"All users have been deleted!", "info")

        return redirect(url_for("home"))


@app.route("/user", methods=["GET", "POST"])
def user():
    email = None

    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email

            found_user = users.query.filter_by(name=user).first()

            if found_user:
                found_user.email = email
                db.session.commit()
                flash(
                    f'Updating email for user "{found_user.name}" to "{email}"!',
                    "info",
                )

        if request.method == "GET":
            if "email" in session:
                email = session["email"]

        return render_template("user.html", user=user, email=email)
    else:
        flash(f"You are not logged in!", "info")
        return redirect(url_for("login"))


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/logout")
def logout():

    flash(f"You have been logged out!", "info")

    session.pop("user", None)
    session.pop("email", None)

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

    with app.app_context():
        db.create_all()
        app.run(debug=True)
