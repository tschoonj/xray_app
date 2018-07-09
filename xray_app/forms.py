from flask_wtf import FlaskForm
from wtforms import StringField, Form
from wtforms.validators import DataRequired, NumberRange

#
                
class xraylib_request(FlaskForm):
    int_z = StringField('Atomic Number', validators=[DataRequired(message="Invalid response"), NumberRange(min=1, max=118)],)
    int_z_error = 'Invalid input - please use an integer'
    

#can then make sub classes for forms that need more input i.e K, L, M etc.
