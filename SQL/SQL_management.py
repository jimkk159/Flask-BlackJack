from flask_login import UserMixin

# self import
from backend.extension import db


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'  # In Local
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


def db_drop_and_create():
    db.drop_all()
    db.create_all()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
