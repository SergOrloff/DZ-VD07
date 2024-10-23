from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('ФИО пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    user_image = FileField('Загрузите фото', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже используется. Пожалуйста, выберите другой.')

class UpdateProfileForm(FlaskForm):
    username = StringField('ФИО пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Новый пароль', validators=[Length(min=6)])
    user_image = FileField('Изображение профиля')
    submit = SubmitField('Обновить профиль')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже используется. Пожалуйста, выберите другой.')