import os
from flask import Flask, render_template

from kodlayalim.config import Config
from kodlayalim.extensions import db, migrate, login

from kodlayalim.routes.home import home_bp
from kodlayalim.routes.auth import auth_bp
from kodlayalim.routes.profile import profile_bp
from kodlayalim.routes.course import course_bp

def forbidden(e):
  return render_template('403.html'), 403

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
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(course_bp, url_prefix='/courses')

    app.register_error_handler(403, forbidden)


    return app
