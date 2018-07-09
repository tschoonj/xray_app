from flask import render_template, request, url_for
from xray_app import app
from xray_app.forms import xraylib_request
import xraylib

def validate_int(input):
        if type(input) != int:
               return xraylib_request.int_z_error

@app.route("/")
def index():
        return render_template('index.html') 

@app.route('/atomicweight', methods=['GET', 'POST'])
def atomicweight():
        form = xraylib_request()
        if request.method == 'POST':
                #for key in request.form.keys():
                #        print(f'key= {key}')
                int_z = request.form['int_z']
                if 0<int(int_z)<=118:                
                        print(f'int_z: {int_z}')
                        weight = xraylib.AtomicWeight(int(int_z))
                        return render_template('atomicweight.html', title='Atomic Weight', form=form, int_z=int_z, weight=weight)
                else:
                        validate_int(int_z)
                        return render_template('atomicweight.html', title='Atomic Weight', form=form, int_z=int_z, error=xraylib_request.int_z_error)                       
        return render_template('atomicweight.html', title='Atomic Weight', form=form)
  
#url_for('static', filename='style.css')
    
