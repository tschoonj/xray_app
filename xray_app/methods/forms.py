from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class Xraylib_Request(FlaskForm):

    int_z = StringField(
    'Atomic Number', 
    validators=[DataRequired(message="Invalid response"), 
    NumberRange(min=1, max=118)]
    )
   
    float_q = StringField(
    'Momentum Transfer', 
    validators=[DataRequired(message="Invalid response")]
    )
    #submit = SubmitField(
    #'Submit',
    #validators=[DataRequired(message="Invalid response")])

#def Function_Request(Flaskform):
    #function = SelectField('Select Function', validators=[DataRequired(message="Invalid response")])
      
# set up function to only run the chosen xraylib method, might work better if it is a form
          
class Request_Error():
        int_z_error = 'Invalid input: please enter an integer.'
        float_q_error = 'Invalid input : please enter an number.'
        error = 'Please enter valid input.'
#then when you need error you do error = request_error.error_name
