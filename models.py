"""Database models."""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column( db.Integer, primary_key=True )
    username = db.Column( db.String(100), nullable=False, unique=False)
    email = db.Column( db.String(40), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False )
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False )
