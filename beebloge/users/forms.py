from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from beebloge.models import User
from flask import flash


class LoginForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Hasło', validators=[DataRequired()])
    submit      = SubmitField('Zaloguj')


class RegistrationForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email()])
    username    = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password    = PasswordField('Hasło',
                                validators=[DataRequired(),
                                EqualTo('pass_confirm',
                                message='Wpisano różne hasła!')])
    pass_confirm = PasswordField('Potwierdź hasło', validators=[DataRequired()])
    submit       = SubmitField('Register!')

    def check_email(self):
        if User.query.filter_by(email=self.email.data).first():
            flash('Ten email został już użyty!')
            # raise ValidationError('Your email has been registered already!')
            return False
        return True

    def check_username(self):
        if User.query.filter_by(first_name=self.username.data).first():
            flash('Wybrana nazwa użytkownika jest niedostępna')
            # raise ValidationError('Your username has been registered already!')
            return False
        return True


class UpdateUserForm(RegistrationForm):
    picture = FileField('Załaduj obraz', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Aktualizuj!')
