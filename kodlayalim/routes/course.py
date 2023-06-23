from flask import Blueprint
from flask import flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required

from kodlayalim.decorators import authorize
from kodlayalim.models import db, Course, CourseSection, Answer
from kodlayalim.forms import CourseForm

course_bp = Blueprint('course', __name__)

@course_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    courses = Course.query.order_by(Course.name.asc()).paginate(page=page, per_page=4, error_out=False)
    return render_template('courses/index.html', title='Dersler', courses=courses)

@course_bp.route('/my')
@login_required
@authorize('teacher')
def my():
    page = request.args.get('page', 1, type=int)
    courses = current_user.courses.order_by(Course.name.asc()).paginate(page=page, per_page=4, error_out=False)
    return render_template('courses/my.html', title='Derslerim', courses=courses)

@course_bp.route('/new', methods=['GET', 'POST'])
@login_required
@authorize('teacher')
def create():
    form = CourseForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            course = Course(
                name=form.name.data,
                code=form.code.data,
                description=form.description.data,
                owner_id=current_user.id
            )
            db.session.add(course)
            db.session.commit()

            flash('Ders başarıyla oluşturuldu', 'success')

            return redirect(url_for('course.my'))

    return render_template('courses/new.html', title='Derslerim', form=form)

@course_bp.route('/<int:course_id>')
@login_required
def show(course_id):
    page = request.args.get('page', 1, type=int)
    course = Course.query.get(course_id)
    sections = course.sections.order_by(CourseSection.order.asc()).paginate(page=page, per_page=2, error_out=False)
    current_answer = Answer.query.filter_by(user_id=current_user.id, course_id=course_id).first()

    if not course:
        flash("Böyle bir ders bulunamadı",  "error")
        return redirect(url_for('course.index'))

    return render_template('courses/show.html', title=course.name, course=course, sections=sections, current_answer=current_answer)

@course_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
@authorize('teacher')
def edit(course_id: int):
    course = Course.query.get(course_id)

    if not course:
        flash("Böyle bir ders bulunamadı",  "error")
        return redirect(url_for('course.index'))

    form = CourseForm(data={
        'name': course.name,
        'code': course.code,
        'description': course.description
    })

    if request.method == 'POST':
        if form.validate_on_submit():
            course.name=form.name.data
            course.code=form.code.data
            course.description=form.description.data

            db.session.commit()

            flash('Ders başarıyla güncelledi', 'success')
            return redirect(url_for('course.show', course_id=course.id))

    return render_template('courses/edit.html', title='{} Dersini Güncelle'.format(course.code), course=course, form=form)
