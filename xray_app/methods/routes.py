from flask import Blueprint, render_template, request, url_for
#from xray_app import app - remove me?
from xray_app.methods.forms import Xraylib_Request, Request_Error, Function_Request, Request_Units
import xraylib

methods = Blueprint('methods', __name__)

#eventually move to own package e.g. xray_app.methods.validators, then import
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
#------------------------------------------------------------------------------------------------------------
@methods.route("/", methods=['GET', 'POST'])
def index():
        form = Xraylib_Request()
        function_form = Function_Request()
        
        if request.method == 'POST':
         #need to specify which xraylib method to use with AND statement
                
                for key in request.form.keys():
                    print(f'key= {key}')
                
                select_input = request.form.get('function')
                
                int_z = request.form['int_z']
                float_q = request.form['float_q']
                
                
                if select_input == 'AtomicWeight':
                    if validate_int(int_z) == False:    
                            return render_template(
                            'index.html',
                            form=form,
                            function_form=function_form, 
                            error=Request_Error.int_z_error, 
                            #got to set HTML attr to selected?
                            ) 
                
                    elif 0<int(int_z)<=118:                
                            print(f'int_z: {int_z}')
                            weight = xraylib.AtomicWeight(int(int_z))
                            return render_template(
                            'index.html', 
                            form=form,
                            function_form=function_form,
                            output=weight,
                            units = Request_Units.AtomicWeight_u
                            )
                
                    else:
                            return render_template(
                            'index.html', 
                            form=form,
                            error=Request_Error.int_z_error,
                            function_form=function_form
                            )    
                elif select_input == 'ElementDensity':
                    if validate_int(int_z) == False:    
                            return render_template(
                            'index.html',
                            form=form,
                            function_form=function_form, 
                            error=Request_Error.int_z_error,
                            ) 
                
                    elif 0<int(int_z)<=118:                
                            print(f'int_z: {int_z}')
                            density=xraylib.ElementDensity(int(int_z))
                            return render_template(
                            'index.html', 
                            form=form,
                            function_form=function_form,
                            output=density,
                            units = Request_Units.ElementDensity_u
                            )
                
                    else:
                            return render_template(
                            'index.html', 
                            form=form,  
                            error=Request_Error.int_z_error,
                            function_form=function_form
                            )
                            
                elif select_input == 'Rayl_FF':
                    if validate_int(int_z) == True and validate_float(float_q) == True:
                            print(f'int_z: {int_z}' + f'float_q: {float_q}')
                            rayl_ff=xraylib.Rayl_FF(int(int_z), float(float_q))
                            return render_template(
                            'index.html', 
                            form=form,
                            function_form=function_form,
                            output=rayl_ff,
                            units = Request_Units.ElementDensity_u
                            )    
                        
        return render_template('index.html', form=form, function_form=function_form) 

        
#------------------------------------------------------------------------------------------------------------
@methods.route('/rayleigh_ff', methods=['GET', 'POST'])
def rayleigh_form_factor():
        form = Xraylib_Request()
       
        if request.method == 'POST':
                int_z = request.form['int_z']
                float_q = request.form['float_q']
                
                if validate_int(int_z) == False:
                        return render_template(
                        'rayleigh_ff.html', 
                        title='Rayleigh Form Factor', 
                        form=form, 
                        int_z=int_z, 
                        float_q=float_q, 
                        error=Request_Error.int_z_error
                        )
                       
                elif validate_float(float_q) == False:
                        return render_template(
                        'rayleigh_ff.html', 
                        title='Rayleigh Form Factor', 
                        form=form, 
                        int_z=int_z, 
                        float_q=float_q, 
                        error=Request_Error.float_q_error
                        ) 
                elif 0<int(int_z)<=118:                
                        print(f'int_z: {int_z}')
                        rff = xraylib.FF_Rayl(int(int_z), float(float_q))
                        return render_template(
                        'rayleigh_ff.html', 
                        title='Rayleigh Form Factor', 
                        form=form, 
                        int_z=int_z, 
                        float_q=float_q,
                        output = rff
                        )
                else:
                        return render_template(
                        'rayleigh_ff.html', 
                        title='Rayleigh Form Factor', 
                        form=form, 
                        int_z=int_z, 
                        float_q=float_q, 
                        error=Request_Error.error
                        )                       
        return render_template(
        'rayleigh_ff.html', 
        title='Rayleigh Form Factor', 
        form=form
        )  
