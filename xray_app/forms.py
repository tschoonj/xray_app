from flask_wtf import Form
from wtforms import StringField, Form
from wtforms.validators import DataRequired, NumberRange

def validate_int(self, input):
        if type(input) != int:
                raise ValidationError('Error: Not an integer')
                
class xraylib_request(Form):
    atm_num = StringField('Atomic Number', validators=[DataRequired(message="Invalid response"), NumberRange(min=1, max=118)],)
    

#can then make sub classes for forms that need more input i.e K, L, M etc.
