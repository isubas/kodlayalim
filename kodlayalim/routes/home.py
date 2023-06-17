from flask import Blueprint
from flask import render_template
from flask_login import login_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def index():
    return render_template('home/index.html', title='Ana Sayfa')
