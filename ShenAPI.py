import os
from flask import Flask, request, jsonify, render_template, session, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    if not session.get("logged_in"):
        return render_template("login.html")
    else:
        return render_template("home.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return render_template("login.html")
    user.authenticated = True
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=remember)
    session["logged_in"] = True
    return home()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        check_email = User.query.filter_by(email=email).first()
        check_name = User.query.filter_by(name=name).first()

        if (name or email or password or confirm_password) is "":
            flash("Please check your sign up details and try again.")
        elif check_email:
            flash('This email address already exists')
        elif check_name:
            flash('This username already exists')
        elif not (password == confirm_password):
            flash("The password and confirmation password do not match.")
        else:
            encrypted_password = generate_password_hash(request.form.get(password), method="sha256")

            try:
                user = User(
                    name = name,
                    email = email,
                    password = encrypted_password
                )
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                session["logged_in"] = True
                home()
            except Exception as e:
                return (str(e))
    return render_template("signup.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    session["logged_in"] = False
    return home()


@app.route("/users/<name>")
def get_user_name(name):
    return "name : {}".format(name)


@app.route("/getall")
def get_all():
    try:
        users = User.query.all()
        return jsonify([e.serialize() for e in users])
    except Exception as e:
        return (str(e))


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        user = User.query.filter_by(id = id_).first()
        return jsonify(user.serialize())
    except Exception as e:
        return (str(e))


@app.route("/add", methods=["GET", "POST"])
def add_user_form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"), method="sha256")
        try:
            user = User(
                name = name,
                email = email,
                password = password
            )
            db.session.add(user)
            db.session.commit()
            return "User has been added successfully. id = {}".format(user.id)
        except Exception as e:
            return (str(e))
    return render_template("adduser.html")


@app.route("/deleteall")
@login_required
def delete_all_users():
    try:
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return "Deleted all database entries."
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run()