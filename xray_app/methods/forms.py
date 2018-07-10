from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, NumberRange

class Xraylib_Request(FlaskForm):
    int_z = StringField(
    'Atomic Number', 
    validators=[DataRequired(message="Invalid response"), 
    NumberRange(min=1, max=118)]
    )
    float_q = StringField(
    'Momentum Transfer', 
    validators=[DataRequired(message="Invalid response")])  
  
class Request_Error():
        int_z_error = 'Invalid input: please enter an integer.'
        float_q_error = 'Invalid input : please enter an number.'
        error = 'Please enter valid input.'
#then when you need error you do error = request_error.error_name
