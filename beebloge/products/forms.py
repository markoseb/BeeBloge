from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed
from flask import flash


class ProductForm(FlaskForm):
    title       = StringField('Nazwa produktu', validators=[DataRequired()])
    category    = StringField('Kategoria', validators=[DataRequired()])
    text        = CKEditorField('Opis', validators=[DataRequired()])
    picture     = FileField('Zdjęcie', validators=[FileAllowed(['jpg', 'png'])])
    submit      = SubmitField('Opublikuj')

    def check_title(self):
        if len(self.title.data) > 35:
            flash('Nazwa produktu nie może być dłuższa niż 35 znaków')
            # raise ValidationError('Your email has been registered already!')
            return False
        return True
