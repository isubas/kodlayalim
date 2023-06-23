import os
from flask import Flask, render_template
import time

from kodlayalim.config import Config
from kodlayalim.extensions import db, migrate, login

from kodlayalim.routes.auth import auth_bp
from kodlayalim.routes.course import course_bp
from kodlayalim.routes.files import files_bp
from kodlayalim.routes.home import home_bp
from kodlayalim.routes.profile import profile_bp
from kodlayalim.routes.section import section_bp
from kodlayalim.routes.mail import mail_bp
from kodlayalim.routes.quiz import quiz_bp

def forbidden(e):
    return render_template('403.html'), 403

def not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__, template_folder='views')
    app.config.from_object(Config)

    # DB configuration
    db.init_app(app)
    migrate.init_app(app, db, migrate.init_app(app, db, directory=os.path.join(app.config['APP_DIR'], 'migrations')))

    # login configuration
    login.init_app(app)
    login.login_view = 'auth.login'

    # router registry
    app.register_blueprint(home_bp, url_prefix='')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(course_bp, url_prefix='/courses')
    app.register_blueprint(files_bp, url_prefix='/files')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(section_bp, url_prefix='/courses/<int:course_id>/sections')
    app.register_blueprint(mail_bp, url_prefix='/mail')
    app.register_blueprint(quiz_bp, url_prefix='/courses/<int:course_id>/quiz')

    # error pages
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)

    # filters
    @app.template_filter()
    def get_time(timestamp):
        return time.ctime(timestamp)

    return app
