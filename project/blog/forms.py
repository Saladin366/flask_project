from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])


class CommentForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
