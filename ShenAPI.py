import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import User


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/users/<name>")
def get_user_name(name):
    return "name : {}".format(name)


# @app.route('/add')
# def add_user():
#     name = request.args.get('name')
#     password = request.args.get('password')
#     try:
#         user = User(
#             name = name,
#             password = password
#         )
#         db.session.add(user)
#         db.session.commit()
#         return "User added. user id = {}".format(user.id)
#     except Exception as e:
#         return (str(e))


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


@app.route("/add", methods = ['GET', 'POST'])
def add_user_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
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


if __name__ == '__main__':
    app.run()