from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError


class CountryForm(FlaskForm):
    name = TextField("Name", [validators.Required("Please enter country name.")])
