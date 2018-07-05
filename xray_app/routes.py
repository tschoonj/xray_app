from flask import render_template, request, flash
from xray_app import app
from xray_app.forms import xraylib_request

@app.route("/")
def index():
        return render_template('index.html') 

@app.route('/atomicweight', methods=['GET', 'POST'])
def atomicweight():
        form = xraylib_request()
        if request.method == 'GET':
                for key in request.form.keys():
                        print('key= {}', key)
        
              
        return render_template('atomicweight.html', title='Atomic Weight', form=form)

   #xraylib.AtomicWeight(input)    
 
    
