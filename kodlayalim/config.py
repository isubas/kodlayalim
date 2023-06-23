import os

class Config(object):
    APP_DIR = os.path.dirname(__file__)
    UPLOAD_DIR = os.path.join(APP_DIR, 'uploads')
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(APP_DIR, 'kodlayalim.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY="194a4cb7e0034bd98829ec655b48a779"