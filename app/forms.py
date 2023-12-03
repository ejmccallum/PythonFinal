""" This file contains the forms for the application. """

from flask_wtf import FlaskForm
from wtforms import StringField, \
    validators


class GradeEditForm(FlaskForm):  # type: ignore
    """Grade editor form for the application.
    Args:
        Form (_type_): WTForms class.
    """
    student = StringField('Student', [validators.Length(min=4, max=25)])
    grade = StringField('Grade', [validators.InputRequired()])
    assignment = StringField('Assignment', [validators.InputRequired()])
