from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.model import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(10))
    session_id = db.Column(db.String(50), nullable=True)
    session_id_status = db.Column(db.Boolean, nullable=True)
    hard_expiration_time = db.Column(db.DateTime, nullable=True)
    token = db.Column(db.String(100), nullable=True)
    token_status = db.Column(db.Boolean, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return '<User name={} id={}>'.format(self.username, self.id)
