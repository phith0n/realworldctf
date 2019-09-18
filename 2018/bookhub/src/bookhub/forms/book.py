from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, StopValidation, URL, Length


class BookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 256)])
    description = TextAreaField('description')
    img = StringField('cover', validators=[URL(), Length(1, 256)])
