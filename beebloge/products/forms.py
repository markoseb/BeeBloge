from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import  CKEditorField
from flask_wtf.file import FileField,FileAllowed

class ProductForm(FlaskForm):
    title = StringField('Nazwa produktu', validators=[DataRequired()])
    category = StringField('Kategoria',validators=[DataRequired()])
    text = CKEditorField('Opis', validators=[DataRequired()])
    picture = FileField('Zdjęcie', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Opublikuj')