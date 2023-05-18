from functools import wraps
from flask import flash
from flask_login import current_user
from flask import abort

def authorize(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user is None or current_user.role.name not in roles:
                flash('Bu işlem için yetkisiz yok')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator