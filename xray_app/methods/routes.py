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
                
def validate_str(s):
        try:
            str(s)
            return True
        except ValueError:
            return False

#def validate_NIST(s)
#------------------------------------------------------------------------------------------------------------
nist_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('NIST')}
rad_dict = {xraylib.GetRadioNuclideDataByIndex(int(v))['name']: k for k, v in xraylib.__dict__.items() if k.startswith('RADIO')}
shell_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('SHELL')}
ck_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('TRANS')}
aug_dict = {}
trans_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('_LINE')} #needs to split into 2 tuples for diff select fields S or I and then I has 2 fields
  
nist_tup = [(v, k) for k, v in nist_dict.items()]
rad_name_tup = [(k, v) for k, v in rad_dict.items()]
shell_tup = [(k, k) for k, v in shell_dict.items()]
ck_tup = [(v, k) for k, v in ck_dict.items()] #need to map more useful names - is it poss to do similar thing as rad_nuc 
trans_tup = [(v, k) for k, v in trans_dict.items()]
#print(trans_tup)


#------------------------------------------------------------------------------------------------------------
@methods.route("/", methods=['GET', 'POST'])
def index():
        form = Xraylib_Request()
        form.rad_nuc_name.choices = rad_name_tup
        form.shell.choices =  shell_tup
        form.nistcomp.choices = nist_tup
        form.cktrans.choices = ck_tup
        form.linetype.trans_req.choices = trans_tup 
        #after separating trans_tup - need if statement on radio click so only relevant trans show JQuery 
           
        if request.method == 'POST':        
               #for key in request.form.keys():
                   #print(f'key= {key}')
                
                select_input = request.form.get('function')
                rad_nuc_name = request.form.get('rad_nuc_name')
                shell = request.form.get('shell')
                cktrans = request.form.get('cktrans')
                
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
                    print (f'rad_nuc_name: {rad_nuc_name}')
                    nuc_data = xraylib.GetRadioNuclideDataByName(str(rad_nuc_name))
                    return render_template(
                            'index.html', 
                            form=form,
                            output=nuc_data
                            )
                            
                elif select_input == 'EdgeEnergy':
                    if validate_int(int_z) == True:
                        print(f'int_z: {int_z}' + f'shell: {shell}')
                        #edge_energy=xraylib.EdgeEnergy(int(int_z), xraylib.shell)
                        #doesn't work bc shell isnt in xraylib but
                            
        return render_template('index.html', form=form) 

