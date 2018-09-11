from flask import Blueprint, render_template, request, url_for, make_response
from xray_app.main.forms import Xraylib_Request_Plot
from xray_app.methods.utils import calc_output, all_trans

from matplotlib.backends.backend_svg import FigureCanvasSVG as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import numpy as np

import xraylib

from xray_app.methods.routes import cs_dict, trans_S_tup, trans_I_tup, make_tup, validate_int, validate_str, validate_float

main = Blueprint('main', __name__)
#---------------------------------------------------------------------------------
y = []
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
                plot = create_fig(select_input, range_start, range_end, 
                        log_boo_x, log_boo_y, int_z_or_comp)
                script, div = components(plot)
                y[:]=[]
                return render_template('plot.html', form = form, title = 'Plot', script = script, div = div)
            else:
                return render_template('plot.html', form = form, title = 'Plot')
    
        elif select_input.startswith('CS_FluorLine'):
            if validate_int(int_z) or validate_str(int_z):
                if notation == 'IUPAC':
                    plot = create_fig(select_input, range_start, range_end, 
                            log_boo_x, log_boo_y, int_z, trans)
                    script, div = components(plot)
                    y[:]=[]
                    return render_template('plot.html', form = form, title = 'Plot', script = script, div = div)

                elif notation == 'Siegbahn':
                    plot = create_fig(select_input, range_start, range_end, 
                            log_boo_x, log_boo_y, int_z, siegbahn)
                    script, div = components(plot)
                    y[:]=[]
                    return render_template('plot.html', form = form, title = 'Plot', script = script, div = div)      
            else:
                return render_template('plot.html', form = form, title = 'Plot')
    return render_template('plot.html', title = 'Plot', form = form)
#-------------------------------------------------------------------------------------
tools = 'wheel_zoom,reset,hover,box_zoom,save'
tooltips = [('(x, y)', '($x, $y)')]

# Populates y with xraylib data
def get_data(function, array, *variables):
    xrl_function = getattr(xraylib, function)   
    for i in array:
        y.append(calc_output(function, *variables, i))

# Creates array for x axis
def make_array(range_start, range_end):
    range_start = int(range_start)
    range_end = int(range_end)
    step = (range_end - range_start)*2
    x = np.linspace(range_start, range_end, step)
    return x

# Gets Title for graph
def get_title(*variables):
    t_variables = []
    for variable in variables:
        if validate_int(variable):
            t_variables.append(xraylib.AtomicNumberToSymbol(int(variable)))
        else:
            t_variables.append(str(variable))
    t_variables = ', '.join(t_variables)        
    return t_variables

# Creates Bokeh object        
def create_fig(function, range_start, range_end, log_boo_x, log_boo_y, *variables):
    x = make_array(range_start, range_end)
    get_data(function, x, *variables)
    title = function + ': ' + str(get_title(*variables))
    
    # Sets graph scale depending on input
    if log_boo_y and log_boo_x:
        p = figure(title = title, tools=tools, tooltips=tooltips, sizing_mode='scale_width', 
            x_axis_type = 'log', y_axis_type = 'log', plot_height=500)
    elif log_boo_x:
        p = figure(title = title, tools=tools, tooltips=tooltips, sizing_mode='scale_width', 
            x_axis_type = 'log', plot_height=500)
    elif log_boo_y:
        p = figure(title = title, tools=tools, tooltips=tooltips, sizing_mode='scale_width', 
            y_axis_type = 'log', plot_height=500)
    else:
        p = figure(title = title, tools=tools, tooltips=tooltips, sizing_mode='scale_width', plot_height=500)   
    p.xaxis.axis_label = 'Energy (keV)'
    p.yaxis.axis_label = 'Cross Section (cm^2/g)'
    p.line(x, y)
    p.hover.mode = 'vline'        
    return p

