from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import  CKEditorField
from flask_wtf.file import FileField,FileAllowed

class BlogPostForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    category = StringField('Kategoria',validators=[DataRequired()])
    text = CKEditorField('Text', validators=[DataRequired()])
    picture = FileField('Grafika', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Opublikuj')

