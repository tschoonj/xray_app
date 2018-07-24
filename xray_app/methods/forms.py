from flask import g 
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import xraylib #move with dicts later


class Xraylib_Request(FlaskForm):
    comp = StringField('Compound',validators=[DataRequired()])
    int_z = StringField('Element',validators=[DataRequired()])
    int_z_or_comp = StringField('Element or Compound',validators=[DataRequired()]) #needs to accomodate both str and int - try/except loop!
    float_q = StringField('Momentum Transfer',validators=[DataRequired()])
    energy = StringField('Energy', validators=[DataRequired()])
    theta = StringField(u'Theta &#952', validators=[DataRequired()])
    phi = StringField(u'Phi &#981', validators=[DataRequired()])
    density = StringField('Density',validators=[DataRequired()])
    pz = StringField('Electron Momentum p<sub>z</sub>',validators=[DataRequired()])
    linetype = SelectField(u'Transition', 
        choices=[],
        validators=[DataRequired()]) 
        #needs to have a choice of IUPAC, SIEGBAHN or ALL 
        #can do with dynamic select field will need extra select field though  
    shell = SelectField(u'Shell', 
        choices=[],
        validators=[DataRequired()])
    cktrans = SelectField(u'Coster Kronig Trans', 
        choices=[],
        validators=[DataRequired()])
    nistcomp = SelectField(u'NIST Compound', 
        choices=[],
        validators=[DataRequired()])
    augtrans = SelectField(u'Auger Transition', 
        choices=[],
        validators=[DataRequired()])
    rad_nuc_index = SelectField(u'Radio Nuclide I', 
        choices=[],
        validators=[DataRequired()])
    rad_nuc_name = SelectField(u'Radio Nuclide N', 
        choices=[],
        validators=[DataRequired()])
    function = SelectField(u'Xraylib Function', 
        choices=[('AtomicWeight', 'Atomic Weight'), ('ElementDensity', 'Element Density'), ('FF_Rayl', 'Rayleigh Form Factor'), ('LineEnergy','Fluorescence Line Energy'), ('EdgeEnergy','Absorption Edge Energy'), ('RadRate','Radiative Transition Probability'), ('JumpFactor','Jump Ratio'), ('FluorYield','Fluorescence Yield'), ('AugerYield','Auger Yield'), ('AtomicLevelWidth','Atomic Level Width'), ('ElectronConfig','Electronic Configuration'), ('CS_Photo_Partial','Partial Photoionization CS'), ('CS_Total','Total CS'), ('CS_Photo','Photoionization CS'), ('CS_Rayl','Rayleigh CS'), ('CS_Compt','Compton CS'), ('CSb_Total','Total CSb'), ('CSb_Photo','Photoionization CSb'), ('CSb_Rayl','Rayleigh CSb'), ('CSb_Compt','Compton CSb'), ('GetRadioNuclideDataByName', 'Radio Nuclide Excitation Profile')],
        validators=[DataRequired()])    

    #choices(value,label)
      
class Request_Error():
        comp_error = 'Invalid input: Compound'
        int_z_error = 'Invalid input: Element'
        int_z_or_comp_error = 'Invalid input: Element or Compound'
        float_q_error = 'Invalid input : Momentum Transfer.'
        linetype_error = 'Invalid input: Linetype'
        shell_error = 'Invalid input: Shell'
        energy_error = 'Invalid input: Energy'
        theta_error = 'Invalid input: Theta'
        phi_error = 'Invalid input: Phi'
        density_error = 'Invalid input: Density'
        pz_error = 'Invalid input: Pz'
        cktrans_error = 'Invalid input: cktrans'
        nistcomp_error = 'Invalid input: nistcomp'
        augtrans_error = 'Invalid input: augtrans'
        rad_nuc_error = 'Invalid input: rad_nuc_'    
        error = 'Please enter valid input.'
#then when you need error you do error = request_error.error_name
#might be more efficient doing an % if error.xxxx %?

class Request_Units():
        AtomicWeight_u = 'g mol<sup>-1</sup>'
        ElementDensity_u = 'g cm<sup>-3</sup>'
        LineEnergy_u = 'keV'
        EdgeEnergy_u = 'keV'
        RadRate_u = ''
        FluorYield_u = ''
        ElectronConfig_u = ''
        CS_u = 'cm<sup>2</sup> g<sup>-1</sup>'
        CSb_u = ''
        
 #<sup></sup>       
