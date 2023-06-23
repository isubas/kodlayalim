from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, Markup
from flask_login import login_required, current_user

from kodlayalim.models import db, Question, Answer
from kodlayalim.forms import QuizForm

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/', methods=['GET', 'POST'])
@login_required
def index(course_id):
    current_answer = Answer.query.filter_by(user_id=current_user.id, course_id=course_id).first()

    if current_answer:
        flash('Sınavını daha önce tamamlamışsın, tekrar sınava katılamazsın!', 'error')
        return redirect(url_for('course.show', course_id=course_id))

    questions = Question.query.filter_by(course_id=course_id)
    form = QuizForm()

    if request.method == 'POST':
        answers=[]
        total_score = 0
        answer_number = 0
        correct_answer_number = 0
        for question in questions:
            answer_name = 'answer-{}'.format(question.id)
            if answer_name in request.form:
                answer_key = request.form[answer_name]
                answers.append("{}-{}".format(question.id, answer_key))
                answer_number += 1
                if answer_key == question.correct_option:
                    correct_answer_number += 1
                    total_score += question.score

        if answer_number == 0:
            flash('En az 1 soru cevaplamalısın!', 'error')
            return redirect(url_for('quiz.index', course_id=course_id))

        if current_user.role.name == 'student':
            new_answer = Answer(
                course_id = course_id,
                user_id = current_user.id,
                answers = ','.join(answers),
                score = total_score,
                answer_number = answer_number,
                correct_answer_number = correct_answer_number
            )

            db.session.add(new_answer)
            db.session.commit()

        flash('Sınavın tamamlandı!', 'success')
        return render_template('quiz/score.html', title="Quiz Puanı", answer_number=answer_number, correct_answer_number=correct_answer_number, total_score=total_score)

    return render_template('quiz/index.html', title="Quiz", questions=questions, form=form)
