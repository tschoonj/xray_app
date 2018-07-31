from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class Xraylib_Request_Plot(FlaskForm):
    function = SelectField(
        u'Xraylib Function',
        choices = [],
        validators = [DataRequired()]
        )
    range_start = StringField(
        u'Start',
        validators = [DataRequired()]
        ) 
    range_end = StringField(
        u'End',
        validators = [DataRequired()]
        )
