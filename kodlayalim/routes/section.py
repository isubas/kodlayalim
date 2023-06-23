from flask import Blueprint
from flask import flash, redirect, request, render_template, url_for
from flask_login import login_required, current_user

from kodlayalim.decorators import authorize
from kodlayalim.models import db, Course, CourseSection, Comment
from kodlayalim.forms import CourseSectionForm, CommentForm

section_bp = Blueprint('section', __name__)

@section_bp.route('/new', methods=['GET', 'POST'])
@login_required
@authorize('teacher')
def new(course_id: int):
    course = Course.query.filter_by(id=course_id, owner_id=current_user.id).first()

    if not course:
        flash('Sistemde bu ders kaydı bulunamadı', 'error')
        return redirect(url_for('course.index'))

    form = CourseSectionForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            section = CourseSection(
                title=form.title.data,
                body=form.body.data, course_id=course_id,
                order=form.order.data
            )
            db.session.add(section)
            db.session.commit()

            flash('Ders bölümü başarıyla oluşturuldu', 'success')

            return redirect(url_for('course.show', course_id=course_id))

    return render_template('sections/new.html', title='Ders Bölümü Ekle', form=form, course=course)

@section_bp.route('/<int:sid>/edit', methods=['GET', 'POST'])
@login_required
@authorize('teacher')
def edit(course_id, sid):
    course = Course.query.filter_by(id=course_id, owner_id=current_user.id).first()

    if not course:
        flash('Sistemde bu ders kaydı bulunamadı', 'error')
        return redirect(url_for('course.index'))

    section = course.sections.filter_by(id=sid).first()

    if not section:
        flash('Bu ders için bölüm kaydı bulunamadı!', 'error')
        return redirect(url_for('course.show', course_id=course_id))

    form = CourseSectionForm(data={
        'title': section.title,
        'body': section.body,
        'order': section.order
    })

    if request.method == 'POST':
        if form.validate_on_submit():
            section.title=form.title.data
            section.body=form.body.data
            section.order=form.order.data

            db.session.commit()

            flash('Bölüm başarıyla güncelledi', 'success')
            return redirect(url_for('course.show', course_id=course_id))

    return render_template('sections/edit.html', title='Ders Bölümü Güncelle', form=form, course=course, section=section)

@section_bp.route('/<int:sid>/delete')
@login_required
@authorize('teacher')
def delete(course_id, sid):
    course = Course.query.filter_by(id=course_id, owner_id=current_user.id).first()

    if not course:
        flash('Sistemde bu ders kaydı bulunamadı', 'error')
        return redirect(url_for('course.index'))

    section = course.sections.filter_by(id=sid).first()

    if not section:
        flash('Bu ders için bölüm kaydı bulunamadı!', 'error')
        return redirect(url_for('course.show', course_id=course_id))

    db.session.delete(section)
    db.session.commit()

    flash('Bölüm başarıyla silindi.', 'success')
    return redirect(url_for('course.show', course_id=course_id))


@section_bp.route('/<int:sid>/comments', methods=['GET', 'POST'])
@login_required
def comment(course_id, sid):
    section = CourseSection.query.filter_by(course_id=course_id, id=sid).first()

    if not section:
        flash('Bu ders için bölüm kaydı bulunamadı!', 'error')
        return redirect(url_for('course.show', course_id=course_id))

    form = CommentForm()

    if request.method == 'POST':
        new_comment = Comment(
            body=form.body.data,
            user_id=current_user.id,
            section_id=sid
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Yorum başarıyla kayıt edildi", "success")

        next_page = request.args.get('next') or url_for('course.show', course_id=course_id)
        return redirect(next_page)

    return render_template('sections/new_comment.html', title="Bölüme Yorum Ekle", form=form, section=section)
