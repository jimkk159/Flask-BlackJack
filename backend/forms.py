from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerRangeField, DecimalRangeField
from wtforms.validators import DataRequired


class SettingForm(FlaskForm):
    decks = IntegerRangeField(label='Deck Number', render_kw={"min": 2, "max": 8, "step": 1})
    players = IntegerRangeField(label='Max Player of Table', render_kw={"min": 1, "max": 4, "step": 1})
    is_insurance = BooleanField('Insurance')
    is_over_10 = BooleanField('Insurance of card over 10')
    is_double = BooleanField('Double Down')
    bj_ratio = DecimalRangeField('Blackjack Odds', render_kw={"min": 1.2, "max": 1.5, "step": 0.1})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Your Name"})
    room = StringField('Room', validators=[DataRequired()], render_kw={"placeholder": "Room Name"})
    submit = SubmitField('Submit')
