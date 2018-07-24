from flask import Blueprint, render_template, request, url_for
#from xray_app import app - remove me?
from xray_app.methods.forms import Xraylib_Request, Request_Error,  Request_Units
import xraylib

methods = Blueprint('methods', __name__)

#eventually move to own package e.g. xray_app.methods.validators, then import
#ditto for the dicts
def validate_int(s):
        try: 
                int(s)
                return True
        except ValueError:
                return False
        
def validate_float(s):
        try: 
                float(s)
                return True
        except ValueError:
                return False

#def validate_NIST(s)
#------------------------------------------------------------------------------------------------------------
NISTdict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('NIST')}

RADtup = [(str(v), str(k)) for k, v in xraylib.__dict__.items() if k.startswith('RADIO')]

#also need trans, shell, cktrans, augtrans, rad_nuc dicts
#------------------------------------------------------------------------------------------------------------
@methods.route("/", methods=['GET', 'POST'])
def index():
        form = Xraylib_Request()
        form.rad_nuc.choices = RADtup
        #n, n[RADdict]) for n in RADdict
       
           
        if request.method == 'POST':        
               #for key in request.form.keys():
                   #print(f'key= {key}')
                
                select_input = request.form.get('function')
                
                int_z = request.form['int_z']
                float_q = request.form['float_q']
                                
                if select_input == 'AtomicWeight':
                    if validate_int(int_z) == True and 0<int(int_z)<=118:                
                            print(f'int_z: {int_z}')
                            weight = xraylib.AtomicWeight(int(int_z))
                            return render_template(
                            'index.html', 
                            form=form,
                            output=weight,
                            units = Request_Units.AtomicWeight_u
                            )
                
                    else:
                            return render_template(
                            'index.html', 
                            form=form,
                            error=Request_Error.int_z_error
                            )
                                
                elif select_input == 'ElementDensity':
                    if validate_int(int_z) == True and 0<int(int_z)<=118:
                            print(f'int_z: {int_z}')
                            density=xraylib.ElementDensity(int(int_z))
                            return render_template(
                            'index.html', 
                            form=form,
                            output=density,
                            units = Request_Units.ElementDensity_u
                            )                
                    else:
                            return render_template(
                            'index.html', 
                            form=form,  
                            error=Request_Error.int_z_error
                            )
                            
                elif select_input == 'FF_Rayl':
                    if validate_int(int_z) == True and validate_float(float_q) == True:
                            print(f'int_z: {int_z}' + f'float_q: {float_q}')
                            rayl_ff=xraylib.FF_Rayl(int(int_z), float(float_q))
                            return render_template(
                            'index.html', 
                            form=form,
                            output=rayl_ff,
                            units = Request_Units.ElementDensity_u
                            )
                    elif validate_float(float_q) == False:
                            return render_template(
                            'index.html', 
                            form=form,  
                            error=Request_Error.float_q_error
                            )
                    else:
                            return render_template(
                            'index.html', 
                            form=form,  
                            error=Request_Error.int_z_error
                            )    
                elif select_input == 'GetRadioNuclideDataByName':
                    print (f'rad_nuc: {rad_nuc}')
                    grndbn = xraylib.GetRadioNuclideDataByName(rad_nuc)
                    return render_template(
                            'index.html', 
                            form=form,
                            output=grndbn
                            )
                            
        return render_template('index.html', form=form) 

