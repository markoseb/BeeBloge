from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment = TextAreaField('Komentarz', validators=[DataRequired()])
    submit  = SubmitField('Opublikuj')
