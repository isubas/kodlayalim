from datetime import datetime
import enum

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from kodlayalim.extensions import db, login

class Role(enum.Enum):
    student = 0
    teacher = 1
    admin = 2

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Enum(Role), default=Role.student, server_default="student", nullable=False)

    # profile
    about_me = db.Column(db.String(255))
    email_public = db.Column(db.Boolean(), default=False, server_default="true", nullable=False)
    avatar = db.Column(db.Text())

    # login details
    last_login = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relations
    courses = db.relationship('Course', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    code = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(1024))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Course {}>'.format(self.name)