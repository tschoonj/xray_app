from flask import Blueprint, render_template, request, url_for, make_response
from xray_app.main.forms import Xraylib_Request_Plot

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import xraylib

from xray_app.methods.routes import cs_dict, make_tup, validate_int

def delete_keys(key, _dict):
    if key in _dict:
        del _dict[key]
        
delete_keys('CS_KN', cs_dict)
cs_tup = make_tup(cs_dict)
#need to remove uncessary functions from cs tup e.g. CN_KN

main = Blueprint('main', __name__)

@main.route("/about")
def about():
    return render_template('about.html', title = 'About ')

@main.route("/plot", methods=['GET', 'POST'])
def plot():
    form = Xraylib_Request_Plot()
    form.function.choices = form.function.choices + cs_tup
    #not all of these are needed delete as necessary
    
    if request.method == 'POST':        
        #for key in request.form.keys():
        #print(f'key= {key}')
                
        select_input = request.form.get('function')
        range_start = request.form['range_start']
        range_end = request.form['range_end']
        
        #int_z = request.form['variable-int_z']
        #float_q = request.form['variable-float_q']
        #comp = request.form['variable-comp']
        int_z_or_comp = request.form['variable-int_z_or_comp']
        energy = request.form['variable-energy']
        #theta = request.form['variable-theta']
        #phi = request.form['variable-phi']
        #density = request.form['variable-density']
        #pz = request.form['variable-pz']
        
        if select_input.startswith('CS'):
            #need validation of requests
            plot = make_plot(select_input, 'Energy ($keV$)', r'Cross Section ($cm^{2} g^{-1}$)', range_start, range_end, int_z_or_comp)
            return render_template('plot.html', form = form, title = 'Plot', plot=plot)
             
        return render_template('plot.html', form = form, title = 'Plot', plot=plot)
           
    return render_template('plot.html', title = 'Plot', form = form)

def print_data(*lsts):
    lst = zip(*lsts)    
    for value in lst:
            print(value)
    
def make_plot(function, xlabel, ylabel, range_start, range_end, variable):
    x = []
    y = [] 
    xrl_function = getattr(xraylib, function)
    if validate_int(variable) == True:
        for i in range(int(range_start), int(range_end), 1):
            x.append(i)
            y.append(float(xrl_function(int(variable), i)))
    else:
        for i in range(int(range_start), int(range_end), 1):
            xrl_function = getattr(xraylib, function + '_CP')
            x.append(i)
            y.append(float(xrl_function(str(variable), i)))     
    #print_data(x, y)
    
    fig = Figure()
    canvas = FigureCanvas(fig)
            
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(title = function + ': ' + variable, xlabel = 'log[ ' + xlabel + ' ]', ylabel = 'log[ ' + ylabel + ' ]')            
    
    #toggle with boolean?
    #plt.yscale('log')
    #plt.xscale('log')
            
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img_bytes = img.getvalue()
    img.close()
    img64 = str(base64.b64encode(img_bytes), encoding='utf-8')
    return img64  
