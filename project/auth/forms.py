from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from .models import User

EQUAL_TO_PASSWORD = 'Пароли должны совпадать'
USER_EXISTS = 'Такой пользователь уже существует'
EMAIL_EXISTS = 'Такая почта уже существует'


class SignUpForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Подтвердите пароль',
        validators=[DataRequired(),
                    EqualTo('password', message=EQUAL_TO_PASSWORD)])

    def validate_username(self, username):
        if User.query.filter_by(username=username.data.lower()).first():
            raise ValidationError(USER_EXISTS)

    def validate_email(self, email):
        if User.query.filter_by(email=email.data.lower()).first():
            raise ValidationError(EMAIL_EXISTS)


class LoginForm(FlaskForm):
    email_login = StringField('Почта или логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
