from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField, BooleanField
from wtforms.validators import DataRequired
from xray_app.methods.forms import TransitionForm

class VariableForm(FlaskForm):
    #comp = StringField('Compound',validators = [DataRequired()])
    #int_z = StringField('Element',validators = [DataRequired()])
    int_z_or_comp = StringField('Element or Compound',validators = [DataRequired()])
    #float_q = StringField('Momentum Transfer',validators = [DataRequired()])
    energy = StringField('Energy', validators = [DataRequired()])
    #theta = StringField(u'Theta &#952', validators = [DataRequired()])
    #phi = StringField(u'Phi &#981', validators = [DataRequired()])
    #density = StringField('Density',validators = [DataRequired()])
    #pz = StringField('Electron Momentum p<sub>z</sub>',validators = [DataRequired()])
    #linetype = FormField(TransitionForm) 
        #needs to have a choice of IUPAC, SIEGBAHN or ALL 
        #can do with dynamic select field will need extra select field though  
    #shell = SelectField(
        #u'Shell', 
        #choices = [],
        #validators = [DataRequired()])
    #cktrans = SelectField(
        #u'Coster Kronig Trans', 
        #choices = [],
        #validators = [DataRequired()])
    #augtrans = SelectField(
        #u'Auger Transition', 
        #choices = [],
        #validators = [DataRequired()])
    
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
    log_boo = BooleanField(
        u'Log Scale'
        )    
    variable = FormField(VariableForm)
