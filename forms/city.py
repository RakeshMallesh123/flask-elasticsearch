from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError


class CityForm(FlaskForm):
    name = TextField("Name", [validators.Required("Please enter city name.")])
    state = TextField("State", [validators.Required("Please enter state name.")])


class EditCityForm(FlaskForm):
    id = TextField("Id", [validators.Required("Please enter id of country.")])
    name = TextField("Name", [validators.Required("Please enter city name.")])
    state = TextField("State", [validators.Required("Please enter state name.")])
