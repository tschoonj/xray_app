from flask import g 
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FormField, RadioField
from wtforms.validators import DataRequired, NumberRange
import xraylib #move with dicts later

class TransitionForm(FlaskForm):
    notation = RadioField(
            u'Notation',
            choices = [('IUPAC','IUPAC'),('Siegbahn','Siegbahn'),('All','All')],
            default = 'IUPAC',
            validators = [DataRequired()])
    iupac1 = SelectField(
            u'Transition', 
            choices = [('K', 'K'), ('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('M4', 'M4'), ('M5', 'M5'), ('N1', 'N1'), ('N2', 'N2'), ('N3', 'N3'), ('N4', 'N4'), ('N5', 'N5'), ('N6', 'N6'), ('N7', 'N7'), ('O1', 'O1'), ('O2', 'O2'), ('O3', 'O3'), ('O4', 'O4'), ('O5', 'O5'), ('O6', 'O6'), ('O7', 'O7'), ('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3'), ('P4', 'P4'), ('P5', 'P5'), ('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3')],
            validators = [DataRequired()])
    iupac2 = SelectField(
            u'Transition', 
            choices = [('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('M4', 'M4'), ('M5', 'M5'), ('N1', 'N1'), ('N2', 'N2'), ('N3', 'N3'), ('N4', 'N4'), ('N5', 'N5'), ('N6', 'N6'), ('N7', 'N7'), ('O1', 'O1'), ('O2', 'O2'), ('O3', 'O3'), ('O4', 'O4'), ('O5', 'O5'), ('O6', 'O6'), ('O7', 'O7'), ('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3'), ('P4', 'P4'), ('P5', 'P5'), ('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3')],
            validators = [DataRequired()])      
    siegbahn = SelectField(
            u'Transition', 
            choices = [],
            validators = [DataRequired()])

class AugerForm(FlaskForm):
    ex_shell = SelectField( u'Excited Shell',
        choices = [('K', 'K'), ('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('M4', 'M4')], 
        validators = [DataRequired()])
    trans_shell = SelectField(u'Transition Shell', 
        choices = [('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('M4', 'M4'), ('M5', 'M5')], 
        validators = [DataRequired()])
    aug_shell = SelectField(u'Auger Electron Shell', 
        choices = [('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('M4', 'M4'), ('M5', 'M5'), ('N1', 'N1'), ('N2', 'N2'), ('N3', 'N3'), ('N4', 'N4'), ('N5', 'N5'), ('N6', 'N6'), ('N7', 'N7'), ('O1', 'O1'), ('O2', 'O2'), ('O3', 'O3'), ('O4', 'O4'), ('O5', 'O5'), ('O6', 'O6'), ('O7', 'O7'), ('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3'), ('P4', 'P4'), ('P5', 'P5'), ('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3')], 
        validators = [DataRequired()])
    
class Xraylib_Request(FlaskForm):
    function = SelectField(
        u'Xraylib Function', 
        choices = [('AtomicWeight', 'Atomic Weight'), ('ElementDensity', 'Element Density'), ('FF_Rayl', 'Rayleigh Form Factor'), ('SF_Compt', 'Incoherent Scattering Factor'), ('LineEnergy','Fluorescence Line Energy'), ('EdgeEnergy','Absorption Edge Energy'), ('RadRate','Radiative Transition Probability'), ('JumpFactor','Jump Factor'), ('FluorYield','Fluorescence Yield'), ('AugerYield','Auger Yield'), ('AugerRate','Auger Rate'), ('AtomicLevelWidth','Atomic Level Width'), ('ElectronConfig','Electronic Configuration'), ('ComptonEnergy', 'Energy after Compton scattering'), ('Fi', u'Anomalous Scattering Factor \u03C6\''), ('Fii', u'Anomalous Scattering Factor \u03C6\'\''), ('CosKronTransProb', 'Coster-Kronig Transition Probability'), ('ComptonProfile', 'Compton Broadening Profile'), ('ComptonProfile_Partial', 'Partial Compton Broadening Profile'),  ('MomentTransf', ('Momentum Transfer')), ('Refractive_Index','Refractive Index'), ('CompoundParser', 'Compound Parser'),  ('GetRadioNuclideDataList', 'Get Radio Nuclide List'), ('GetRadioNuclideDataByIndex', 'Radio Nuclide Excitation Profile'), ('GetCompoundDataNISTList','Get List of NIST Compounds'),  ('GetCompoundDataNISTByIndex','Get NIST Data')],
        default = 'LineEnergy',
        validators = [DataRequired()])
    comp = StringField('Compound', default = 'Ca5(PO4)3', validators = [DataRequired()])
    int_z = StringField('Element', default = '26', validators = [DataRequired()])
    int_z_or_comp = StringField('Element or Compound', default = 'FeSO4', validators = [DataRequired()])
    float_q = StringField('Momentum Transfer', default = '0.57', validators = [DataRequired()])
    energy = StringField('Energy (keV)', default = '10.0', validators = [DataRequired()])
    theta = StringField('Scattering Angle &#952 (rad)', default = '1.57', validators = [DataRequired()])
    phi = StringField(u'Azimuthal Angle &#981 (rad)', default = '3.14', validators = [DataRequired()])
    density = StringField('Density (g cm<sup>-3</sup>)', default = '1.0', validators = [DataRequired()])
    pz = StringField('Electron Momentum p<sub>z</sub>', default = '1.0', validators = [DataRequired()])     
    shell = SelectField(u'Shell', choices = [], validators = [DataRequired()])
    cktrans = SelectField(u'Coster Kronig Trans', choices = [], validators = [DataRequired()])
    nistcomp = SelectField(u'NIST Compound', choices = [], validators = [DataRequired()])    
    rad_nuc = SelectField( u'Radio Nuclide', choices = [], validators = [DataRequired()])
    #choices(value,label)
    #default = ''
    transition = FormField(TransitionForm) 
    augtrans = FormField(AugerForm, u'Auger Transition')
    examples = SelectField(
        u'Code Example', 
        choices = [('cpp-objdump','C/C++/Objective-C'), ('fortran','Fortran 2003/2008'), ('perl','Perl'), ('idl','IDL'), ('python','Python'), ('java','Java'), ('csharp','C#/.NET'), ('lua','Lua'), ('ruby','Ruby'), ('php','PHP')],
        validators = [DataRequired()])
      
#------------------------------------------------------------------------------------------------------------
class Request_Error():
    comp_error = 'Invalid input: Compound'
    int_z_error = 'Invalid input: Element'
    int_z_or_comp_error = 'Invalid input: Element or Compound'
    float_q_error = 'Invalid input : Momentum Transfer.'
    trans_error = 'Invalid input: Transition'
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
#then when you need errors you render error as request_error.error_name 
        
class Request_Units():
    AtomicWeight_u = ' g mol<sup>-1</sup>'
    ElementDensity_u = ' g cm<sup>-3</sup>'
    Energy_u = ' keV'
    ElectronConfig_u = ' electrons'
    CS_u = ' cm<sup>2</sup> g<sup>-1</sup>'
    CSb_u = ' barnes atom<sup>-1</sup>'
    DCS_u = ' cm<sup>2</sup> g<sup>-1</sup> sr<sup>-1</sup>'
    per_u = ' %'
        
 #<sup></sup>       
