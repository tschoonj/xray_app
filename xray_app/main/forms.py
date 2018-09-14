from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField, BooleanField
from wtforms.validators import DataRequired
from xray_app.methods.forms import TransitionForm
    
class Xraylib_Request_Plot(FlaskForm):
    function = SelectField(
        u'Xraylib Function',
        choices = [],
        validators = [DataRequired()]
        )
    range_start = StringField(
        u'Start (keV)',
        default = '0',
        validators = [DataRequired()]
        ) 
    range_end = StringField(
        u'End (keV)',
        default = '100',
        validators = [DataRequired()]
        )
    log_boo_x = BooleanField(
        u'Log Scale (x)'
        )
    log_boo_y = BooleanField(
        u'Log Scale (y)'
        )   
    transition = FormField(TransitionForm)
    int_z = StringField('Element', default = '26', validators = [DataRequired()])
    int_z_or_comp = StringField('Element or Compound', default = 'FeSO4', validators = [DataRequired()])
