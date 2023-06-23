from datetime import datetime
import enum
import os

from flask import current_app
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
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    received_messages = db.relationship('Message', backref='receiver', foreign_keys='Message.receiver_id', lazy='dynamic')
    sent_messages = db.relationship('Message', backref='sender', foreign_keys='Message.sender_id', lazy='dynamic')

    @property
    def upload_dir(self):
        return os.path.join(current_app.config['UPLOAD_DIR'], str(self.id))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def unread_messages_count(self):
        return self.received_messages.filter_by(read=False).count()

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

    # relations
    sections = db.relationship('CourseSection', backref='course', lazy='dynamic')
    questions = db.relationship('Question', backref='course', lazy='dynamic')
    answers = db.relationship('Answer', backref='course', lazy='dynamic')

    def is_questions_exists(self):
        return Question.query.filter_by(course_id=self.id).count() > 0

    def __repr__(self):
        return '<Course {}>'.format(self.name)

class CourseSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    title = db.Column(db.String(140))
    body = db.Column(db.Text())
    order = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # relations
    comments = db.relationship('Comment', backref='section', lazy='dynamic', foreign_keys="Comment.section_id")

    def __repr__(self):
        return '<CourseSection {}>'.format(self.body)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('course_section.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean(), default=False)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.title)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    content = db.Column(db.Text())
    option_a = db.Column(db.String())
    option_b = db.Column(db.String())
    option_c = db.Column(db.String())
    option_d = db.Column(db.String())
    score = db.Column(db.Integer())
    correct_option =  db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Question {}>'.format(self.body)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    answers = db.Column(db.Text())
    score = db.Column(db.Integer())
    answer_number = db.Column(db.Integer())
    correct_answer_number = db.Column(db.Integer())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Answer {}>'.format(self.body)
