import os
from datetime import datetime

from flask import Blueprint, request, url_for
from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from kodlayalim.models import db, User
from kodlayalim.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('E-posta veya parola hatalı', 'error')
                return redirect(url_for('auth.login'))

            user.last_login = datetime.utcnow()
            db.session.commit()

            login_user(user, remember=form.remember_me.data)

            if not os.path.exists(user.upload_dir):
                os.mkdir(user.upload_dir)

            flash('Başarıyla giriş yapıldı.', 'success')

            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home.index')

            return redirect(next_page)
        else:
            flash('Formu gözden geçirin. Geçersiz bilgi girişi!', 'error')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Zaten kayıtlısınız.', 'warning')
        return redirect(url_for('home.index'))

    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            flash('Sisteme kaydınız başarıyla yapıldı. Sisteme giriş yapabilirsiniz', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
