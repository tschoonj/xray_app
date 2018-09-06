from flask import Blueprint, render_template, request, url_for, make_response
from xray_app.main.forms import Xraylib_Request_Plot
from xray_app.methods.utils import calc_output, all_trans

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import xraylib

from xray_app.methods.routes import cs_dict, trans_S_tup, trans_I_tup, make_tup, validate_int, validate_str, validate_float

main = Blueprint('main', __name__)
#---------------------------------------------------------------------------------
# Removing unimplemented functions from rendered choices
def delete_key(key, _dict):
    if key in _dict:
        del _dict[key]
        
delete_key('CS_KN', cs_dict)
delete_key('CS_Total_Kissel', cs_dict)
delete_key('CS_Photo_Partial', cs_dict)
cs_tup = make_tup(cs_dict, 'cs')

#---------------------------------------------------------------------------------
@main.route("/about")
def about():
    return render_template('about.html', title = 'About ')
    
#---------------------------------------------------------------------------------
@main.route("/plot", methods=['GET', 'POST'])
def plot():
    form = Xraylib_Request_Plot()
    
    # Populating select fields
    form.function.choices = form.function.choices + cs_tup
    form.transition.siegbahn.choices = trans_S_tup
    
    if request.method == 'POST':        
        # Get user input        
        select_input = request.form.get('function')
        range_start = request.form['range_start']
        range_end = request.form['range_end']
        log_boo_x = request.form.get('log_boo_x')
        log_boo_y = request.form.get('log_boo_y')
        
        int_z = request.form['int_z']
        int_z_or_comp = request.form['int_z_or_comp']
        
        notation = request.form.get('transition-notation')        
        iupac1 = request.form.get('transition-iupac1')
        iupac2 = request.form.get('transition-iupac2')

        # User Input => valid arg for calc_output
        trans = iupac1 + iupac2 + '_LINE'
        siegbahn = request.form.get('transition-siegbahn')
        
        if (select_input == 'CS_Total' or select_input == 'CS_Photo' 
        or select_input == 'CS_Rayl' or select_input == 'CS_Energy' 
        or select_input == 'CS_Compt'):
            if validate_int(int_z_or_comp) or validate_str(int_z_or_comp):
                plot = make_plot(select_input, 
                    'Energy ($keV$)', 
                    r'Cross Section ($cm^{2} g^{-1}$)', 
                    range_start, 
                    range_end, 
                    log_boo_x, 
                    log_boo_y, 
                    int_z_or_comp)
                return render_template('plot.html', form = form, title = 'Plot', plot=plot)
            else:
                return render_template('plot.html', form = form, title = 'Plot')
    
        elif select_input.startswith('CS_FluorLine'):
            if validate_int(int_z) or validate_str(int_z):
                if notation == 'IUPAC':
                    plot = make_plot(select_input, 
                        'Energy ($keV$)', 
                        r'Cross Section ($cm^{2} g^{-1}$)', 
                        range_start, 
                        range_end, 
                        log_boo_x, 
                        log_boo_y, 
                        int_z,
                         trans)
                    return render_template('plot.html', form = form, title = 'Plot', plot=plot)

                elif notation == 'Siegbahn':
                    plot = make_plot(select_input, 
                        'Energy ($keV$)', 
                        r'Cross Section ($cm^{2} g^{-1}$)', 
                        range_start, 
                        range_end, 
                        log_boo_x, 
                        log_boo_y, 
                        int_z, 
                        siegbahn)
                    return render_template('plot.html', form = form, title = 'Plot', plot=plot)          
            else:
                return render_template('plot.html', form = form, title = 'Plot')
    return render_template('plot.html', title = 'Plot', form = form)
#-------------------------------------------------------------------------------------
def make_plot(function, xlabel, ylabel, range_start, range_end, log_boo_x, log_boo_y, *variables):
    x = []
    y = []
    t_variables = [] 

    if validate_int(range_start, range_end):
        for i in range(int(range_start), int(range_end), 1):
            y.append(float(calc_output(function, *variables, i)))
            x.append(i)        
    elif validate_float(range_start, range_end):
        for i in range(int(float(range_start)), int(float(range_end)), 1):
            y.append(float(calc_output(function, *variables, i)))
            x.append(i)
    else:
        #print('invalid range')
        return
    
    if sum(y) == 0:
        return #Add more useful/specific error message e.g. Line unsupported
    
    fig = Figure()
    canvas = FigureCanvas(fig)
            
    fig, ax = plt.subplots()
    ax.plot(x, y)
    
    # Adds titles to graph
    for variable in variables:
        if validate_int(variable):
            t_variables.append(xraylib.AtomicNumberToSymbol(int(variable)))
        else:
            t_variables.append(str(variable))    
    t_variables = ', '.join(t_variables)
    ax.set(title = function + ': ' + t_variables, xlabel = xlabel, ylabel = ylabel)                

    # Sets graph scale depending on input
    if log_boo_y and log_boo_x:
        plt.xscale('log')                  
        plt.yscale('log')
    elif log_boo_x:
        plt.xscale('log')
    elif log_boo_y:
        plt.yscale('log')        
    
    # Returns img as encoded byte string
    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    plt.close()
    img_bytes = img.getvalue()
    img.close()
    img64 = str(base64.b64encode(img_bytes), encoding='utf-8')
    return img64 
