from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,DateTimeField,FloatField
from wtforms.validators import DataRequired


class MemoForm(FlaskForm):
    title = TextAreaField("What's happening next?", validators=[DataRequired()])
    body = TextAreaField("What you plan to remember?",validators=[DataRequired()])
    time = DateTimeField(validators=[DataRequired()])
    submit = SubmitField("Submit")


class LatLngForm(FlaskForm):
    placename = StringField(validators=[DataRequired()])
    lat = FloatField(validators=[DataRequired()])
    lng = FloatField(validators=[DataRequired()])
    submit = SubmitField("Submit")
