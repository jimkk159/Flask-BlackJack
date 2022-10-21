from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SettingForm(FlaskForm):
    decks = SelectField('Deck Number',
                        choices=[("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8")],
                        default="4")
    players = SelectField('Max Player of Table',
                          choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")], default="1")
    is_insurance = SelectField('Insurance',
                               choices=[("open", "Open"), ("close", "Close")], default="open")
    is_over_10 = SelectField('Insurance of Face card and 10',
                             choices=[("open", "Open"), ("close", "Close")], default="close")
    is_double = SelectField('Double Down',
                            choices=[("open", "Open"), ("close", "Close")], default="open")
    bj_ratio = SelectField('Blackjack Odds',
                           choices=[("1.2", "1.2"), ("1.3", "1.3"), ("1.4", "1.4"), ("1.5", "1.5")], default="1.5")
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Your Name"})
    room = StringField('Room', validators=[DataRequired()], render_kw={"placeholder": "Room Name"})
    submit = SubmitField('Submit')
