from flask import g 
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class Xraylib_Request(FlaskForm):
    #make select field then put all string fields in as subfields? also change stringfields to integer fields where necessary
    comp = StringField('Compound',validators=[DataRequired()])
    int_z = StringField('Element',validators=[DataRequired(), NumberRange(min=1, max=118)])
    int_z_or_comp = StringField('Element or Compound',validators=[DataRequired()])
    float_q = StringField('Momentum Transfer',validators=[DataRequired()])
    linetype = StringField('Transition',validators=[DataRequired()])    
    shell = StringField('Shell',validators=[DataRequired()])
    energy = StringField('Energy', validators=[DataRequired()])
    theta = StringField('Theta', validators=[DataRequired()])
    phi = StringField('Phi', validators=[DataRequired()])
    density = StringField('Density',validators=[DataRequired()])
    pz = StringField('Electron Momentum Pz',validators=[DataRequired()])
    cktrans = StringField('Cktrans',validators=[DataRequired()])
    nistcomp = StringField('Nist Compound',validators=[DataRequired()])
    augtrans = StringField('Auger Trans',validators=[DataRequired()])
    rad_nuc = StringField('Radio Nuclide',validators=[DataRequired()])
        
class Function_Request(FlaskForm):
    functions = SelectField('Select Function', 
        choices=[('AtomicWeight', 'atmw'), ('ElementDensity', 'dens'), ('Rayl_FF', 'rff'),
        ('LineEnergy','lineenergy'), ('EdgeEnergy','absedge'), ('RadRate','radrate'), ('JumpFactor','jumprat'), 
        ('FluorYield','flyield'), ('AugerYield','augyield'), ('AtomicLevelWidth','alw'), 
        ('CS_Photo_Partial','cs_pp'), ('CS_Total','cs_tot'), ('CS_Photo','cs_ph'), ('CS_Rayl','cs_rayl'), 
        ('CS_Compt','cs_compt'), ('CSb_Total','csb_tot'), ('CSb_Photo','csb_ph'), ('CSb_Rayl','csb_rayl'), 
        ('CSb_Compt','csb_compt')],
        validators=[DataRequired()])
    #choices(value,label)
    submit = SubmitField('Submit', validators=[DataRequired()])
    #doesn't make a submit button just checks if it has been submitted
      
# set up function to only run the chosen xraylib method, might work better if it is a form
          
class Request_Error():
        int_z_error = 'Invalid input: Element'
        float_q_error = 'Invalid input : Momentum Transfer.'
        #add in other errors
        error = 'Please enter valid input.'
#then when you need error you do error = request_error.error_name
