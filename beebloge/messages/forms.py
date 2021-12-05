from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class MessageForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email()])
    firstName   = StringField('Imię', validators=[DataRequired()])
    lastName    = StringField('Nazwisko')
    phone       = StringField('Telefon')
    text        = TextAreaField('Wiadomość', validators=[DataRequired()])
    submit      = SubmitField('Wyślij!')
