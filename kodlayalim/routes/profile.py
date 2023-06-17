import base64

from flask import Blueprint, request, url_for
from flask import render_template, flash, redirect
from flask_login import login_required, current_user

from kodlayalim.models import db, User
from kodlayalim.forms import ProfileForm

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/<username>')
@login_required
def show(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Böyle bir kullanıcı mevcut değil",  "error")
        return redirect(url_for('home.index'))

    return render_template('profile/show.html', user=user)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = ProfileForm(data={
        'about_me': current_user.about_me,
        'email_public': current_user.email_public
    })

    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.about_me = form.about_me.data
            current_user.email_public = form.email_public.data
            if form.avatar.data:
                avatar = form.avatar.data.stream.read()
                current_user.avatar = base64.encodebytes(avatar).decode()

            db.session.commit()

            flash('Profil bilginiz başarıyla güncellendi', 'success')

            return redirect(url_for('profile.show', username=current_user.username))

    return render_template('profile/edit.html', form=form)

