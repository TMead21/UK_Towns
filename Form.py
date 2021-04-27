from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm1(FlaskForm):
    searchCentre = SelectField('Select town as centre of search', choices=[], coerce=int, validators=[DataRequired()])
    def __init__(self, choices=None):
        super().__init__()  # calls the base initialisation and then...
        if choices:
            # self.language.choices = [(c.id, c.name) for c in choices]
            self.searchCentre.choices = [(c[0], c[1]) for c in choices]
    submit = SubmitField('Enter Parameters')

class LoginForm2(FlaskForm):
    minimum = SelectField('Minimum Travel', choices=[], coerce=int)
    def __init__(self, choices=None):
        super().__init__()  # calls the base initialisation and then...
        if choices:
            # self.language.choices = [(c.id, c.name) for c in choices]
            self.minimum.choices = [(c[0], c[1]) for c in choices]

class LoginForm3(FlaskForm):
    maximum = SelectField('Maximum Travel', choices=[], coerce=int)
    def __init__(self, choices=None):
        super().__init__()  # calls the base initialisation and then...
        if choices:
            # self.language.choices = [(c.id, c.name) for c in choices]
            self.maximum.choices = [(c[0], c[1]) for c in choices]

class LoginForm4(FlaskForm):
    townNumber = SelectField('How many towns to be displayed', choices=[], coerce=int)
    def __init__(self, choices=None):
        super().__init__()  # calls the base initialisation and then...
        if choices:
            # self.language.choices = [(c.id, c.name) for c in choices]
            self.townNumber.choices = [(c[0], c[1]) for c in choices]
