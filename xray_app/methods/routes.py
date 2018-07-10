from flask import Blueprint, render_template, request, url_for
#from xray_app import app - remove me?
from xray_app.methods.forms import Xraylib_Request, Request_Error #remember to add request classes
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
@methods.route('/atomicweight', methods=['GET', 'POST'])
def atomicweight():
        form = Xraylib_Request()
        if request.method == 'POST':
                #for key in request.form.keys():
                #        print(f'key= {key}')
                
                int_z = request.form['int_z']
                
                if validate_int(int_z) == False:    
                        return render_template(
                        'atomicweight.html',
                        title='Atomic Weight',
                        form=form, int_z=int_z,
                        error=Request_Error.int_z_error
                        ) 
                
                elif 0<int(int_z)<=118:                
                        print(f'int_z: {int_z}')
                        weight = xraylib.AtomicWeight(int(int_z))
                        return render_template(
                        'atomicweight.html', 
                        title='Atomic Weight', 
                        form=form, 
                        int_z=int_z, 
                        function=weight
                        )
                
                else:
                        return render_template(
                        'atomicweight.html', 
                        title='Atomic Weight', 
                        form=form, 
                        int_z=int_z, 
                        error=Request_Error.int_z_error
                        )                       
        return render_template(
        'atomicweight.html', 
        title='Atomic Weight', 
        form=form
        )
        
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
                        function=rff
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
