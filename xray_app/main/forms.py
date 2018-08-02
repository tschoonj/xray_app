from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class Xraylib_Request_Plot(FlaskForm):
    function = SelectField(
        u'Xraylib Function',
        choices = [('AtomicWeight', 'Atomic Weight'), ('ElementDensity', 'Element Density'), ('FF_Rayl', 'Rayleigh Form Factor'), ('LineEnergy','Fluorescence Line Energy'), ('EdgeEnergy','Absorption Edge Energy'), ('RadRate','Radiative Transition Probability'), ('JumpFactor','Jump Ratio'), ('FluorYield','Fluorescence Yield'), ('AugerYield','Auger Yield'), ('AtomicLevelWidth','Atomic Level Width'), ('ElectronConfig','Electronic Configuration'), ('GetRadioNuclideDataByName', 'Radio Nuclide Excitation Profile'), ('GetCompoundDataNISTByName','Get NIST Data')],
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
        
class Units():
    pass

class Labels():
    pass
    
class XLabels(Labels):
    pass
    
class YLabels(Labels):
    pass
