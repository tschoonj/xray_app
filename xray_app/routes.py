from flask import render_template, request, url_for
from xray_app import app
from xray_app.forms import xraylib_request
import xraylib

@app.route("/")
def index():
        return render_template('index.html') 

@app.route('/atomicweight', methods=['GET', 'POST'])
def atomicweight():
        form = xraylib_request()
        if request.method == 'POST':
                #for key in request.form.keys():
                #        print(f'key= {key}')
                atm_num = request.form['atm_num']
                print(f'atm_num: {atm_num}')
                weight = xraylib.AtomicWeight(int(atm_num))
                return render_template('atomicweight.html', title='Atomic Weight', form=form, atm_num=atm_num, weight=weight)
        return render_template('atomicweight.html', title='Atomic Weight', form=form)
  
#url_for('static', filename='style.css')
    
