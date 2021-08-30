from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_ckeditor import  CKEditorField
from flask_wtf.file import FileField,FileAllowed

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('Category',validators=[DataRequired()])
    text = CKEditorField('Text', validators=[DataRequired()])
    picture = FileField('Post Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Opublikuj')