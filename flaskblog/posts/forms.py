from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create')

class UpdatePostForm(FlaskForm):
    title = StringField('Update title', validators=[DataRequired()])
    content = TextAreaField('Update content', validators=[DataRequired()])
    submit = SubmitField('Update')
