from flask import render_template, request, url_for
from xray_app import app
from xray_app.forms import xraylib_request
import xraylib

#def validate_int(s):
#        if s[0] in ('-', '+'):
#                return s[1:].isdigit()
#        return s.isdigit()

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
        

@app.route("/")
def index():
        return render_template('index.html') 
        
@app.route("/about")
def about():
        return render_template('about.html')

@app.route('/atomicweight', methods=['GET', 'POST'])
def atomicweight():
        form = xraylib_request()
        if request.method == 'POST':
                #for key in request.form.keys():
                #        print(f'key= {key}')
                int_z = request.form['int_z']
                if validate_int(int_z) == False:
                        return render_template('atomicweight.html', title='Atomic Weight', form=form, int_z=int_z, error=xraylib_request.int_z_error) 
                elif 0<int(int_z)<=118:                
                        print(f'int_z: {int_z}')
                        weight = xraylib.AtomicWeight(int(int_z))
                        return render_template('atomicweight.html', title='Atomic Weight', form=form, int_z=int_z, weight=weight)
                else:
                        return render_template('atomicweight.html', title='Atomic Weight', form=form, int_z=int_z, error=xraylib_request.int_z_error)                       
        return render_template('atomicweight.html', title='Atomic Weight', form=form)

@app.route('/rayleigh_ff', methods=['GET', 'POST'])
def rayleigh_form_factor():
        form = xraylib_request()
        if request.method == 'POST':
                #for key in request.form.keys():
                #        print(f'key= {key}')
                int_z = request.form['int_z']
                float_q = request.form['float_q']
                if validate_int(int_z) == False:
                        return render_template('rayleigh_ff.html', title='Rayleigh Form Factor', form=form, int_z=int_z, float_q=float_q, error=xraylib_request.int_z_error)
                elif validate_float(float_q) == False:
                        return render_template('rayleigh_ff.html', title='Rayleigh Form Factor', form=form, int_z=int_z, float_q=float_q, error=xraylib_request.float_q_error) 
                elif 0<int(int_z)<=118:                
                        print(f'int_z: {int_z}')
                        rff = xraylib.FF_Rayl(int(int_z), float(float_q))
                        return render_template('rayleigh_ff.html', title='Rayleigh Form Factor', form=form, int_z=int_z, float_q=float_q, rff=rff)
                else:
                        return render_template('rayleigh_ff.html', title='Rayleigh Form Factor', form=form, int_z=int_z, float_q=float_q, error=xraylib_request.error)                       
        return render_template('rayleigh_ff.html', title='Rayleigh Form Factor', form=form)  
#url_for('static', filename='style.css')
 
