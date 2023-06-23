from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import BooleanField, EmailField, FileField, PasswordField, \
StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from kodlayalim.models import User

class LoginForm(FlaskForm):
    email = EmailField('E-posta', validators=[DataRequired('Bu alan gerekli')])
    password = PasswordField('Parola', validators=[DataRequired('Bu alan gerekli')])
    remember_me = BooleanField('Beni hatırla')
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired('Bu alan gerekli'), Length(min=3, max=64, message='Kullanıcı adı en az 3, en fazla 64 karakterden oluşmalı')])
    email = EmailField('E-posta', validators=[DataRequired('Bu alan gerekli'), Email(),  Length(max=120, message="E-posta en fazla 100 karakterden oluşabilir.")])
    first_name = StringField('Ad', validators=[DataRequired('Bu alan gerekli'), Length(max=100, message="Ad en fazla 100 karakterden oluşabilir.")])
    last_name = StringField('Soyad', validators=[DataRequired('Bu alan gerekli'), Length(max=100, message="Soyad en fazla 100 karakterden oluşabilir.")])
    password = PasswordField('Parola', validators=[DataRequired('Bu alan gerekli')])
    password2 = PasswordField('Parola Tekrar', validators=[DataRequired('Bu alan gerekli'), EqualTo('password', message='Parola uyuşmazlığı')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Lütfen farklı bir kullanıcı adı ile kayıtlanmayı deneyin.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Lütfen farklı bir e-posta ile kayıtlanmayı deneyin.')

class ProfileForm(FlaskForm):
    avatar = FileField("Avatar")
    about_me = TextAreaField('Hakkımda', validators=[Length(max=200)])
    email_public = BooleanField('E-posta herkese açık')
    submit = SubmitField('Güncelle')

class CourseForm(FlaskForm):
    name = StringField('Ders Adı', validators=[DataRequired('Bu alan gerekli'), Length(max=255, message='Ders adı en fazla 255 karakterden oluşmalı')])
    code = StringField('Ders Kodu', validators=[DataRequired('Bu alan gerekli'), Length(max=100, message='Ders kodu en fazla 255 karakterden oluşmalı')])
    description = TextAreaField('Açıklama', validators=[Length(max=1024)])
    submit = SubmitField('Oluştur')

class CourseSectionForm(FlaskForm):
    title = StringField('Konu Başlığı', validators=[DataRequired(message="Bu alan gerekli")])
    body = TextAreaField('İçerik', render_kw = {'rows': '5'})
    order = IntegerField('Sırası')
    submit = SubmitField('Kaydet')

class FileUploadForm(FlaskForm):
    file = FileField("Dosya Seç", validators=[DataRequired(message="Bu alan gerekli")])
    submit = SubmitField('Yükle')

class CommentForm(FlaskForm):
    body = TextAreaField('Yorum', validators=[DataRequired(message="Bu alan gerekli")])
    submit = SubmitField('Kaydet')

class MailForm(FlaskForm):
    receiver = SelectField('Alıcı', choices=[])
    title = StringField('Başlık', validators=[DataRequired(message="Bu alan gerekli")])
    body = TextAreaField('İleti', render_kw = {'rows': '10'})
    submit = SubmitField('Gönder')

    def __init__(self):
        super(MailForm, self).__init__()
        userlist = User.query.filter(User.id != current_user.id).order_by(User.first_name.asc()).all()
        self.receiver.choices = [(str(user.id), user.full_name) for user in userlist]

class QuizForm(FlaskForm):
    submit = SubmitField('Kaydet')