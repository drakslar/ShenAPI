from ShenAPI import db, app
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.authenticated = False

    def __repr__(self):
        return '<id {}'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'authenticated': self.authenticated
        }

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymus(self):
        return False

    def get_id(self):
        return str(self.id)