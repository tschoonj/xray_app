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
        u'Start',
        validators = [DataRequired()]
        ) 
    range_end = StringField(
        u'End',
        validators = [DataRequired()]
        )
    log_boo_x = BooleanField(
        u'Log Scale (x)'
        )
    log_boo_y = BooleanField(
        u'Log Scale (y)'
        )   
    linetype = FormField(TransitionForm)
    int_z = StringField('Element',validators = [DataRequired()])
    int_z_or_comp = StringField('Element or Compound: ',validators = [DataRequired()])
    shell = SelectField(
        u'Shell', 
        choices = [],
        validators = [DataRequired()])
        
    #comp = StringField('Compound',validators = [DataRequired()])    
    #float_q = StringField('Momentum Transfer',validators = [DataRequired()])
    #energy = StringField('Energy', validators = [DataRequired()])
    #theta = StringField(u'Theta &#952', validators = [DataRequired()])
    #phi = StringField(u'Phi &#981', validators = [DataRequired()])
    #density = StringField('Density',validators = [DataRequired()])
    #pz = StringField('Electron Momentum p<sub>z</sub>',validators = [DataRequired()])
    #cktrans = SelectField(
        #u'Coster Kronig Trans', 
        #choices = [],
        #validators = [DataRequired()])
    #augtrans = SelectField(
        #u'Auger Transition', 
        #choices = [],
        #validators = [DataRequired()])
