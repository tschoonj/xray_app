# Bokeh backend for plotting
from bokeh.plotting import figure
import numpy as np

import xraylib
from xray_app.methods.utils import calc_output
from xray_app.methods.routes import validate_int

tools = 'wheel_zoom,reset,hover,box_zoom,save'
tooltips = [('(x, y)', '($x, $y)')]
y = []

# Populates y with xraylib data
def get_data(function, array, *variables):
    xrl_function = getattr(xraylib, function)
    y[:] = []
    for i in array:
        y.append(calc_output(function, *variables, i))

# Creates array for x axis
def make_array(range_start, range_end):
    range_start = int(range_start)
    range_end = int(range_end)
    step = (range_end - range_start) * 2
    x = np.linspace(range_start, range_end, step)
    return x

# Gets title for graph
def get_title(*variables):
    t_variables = []
    for variable in variables:
        if validate_int(variable):
            t_variables.append(xraylib.AtomicNumberToSymbol(int(variable)))
        else:
            t_variables.append(str(variable))
    t_variables = ', '.join(t_variables)        
    return t_variables
    
# Creates Bokeh model        
def create_fig(function, range_start, range_end, log_boo_x, log_boo_y, *variables):
    # Generates data for plot
    x = make_array(range_start, range_end)
    get_data(function, x, *variables)    
    title = function + ': ' + str(get_title(*variables))
    
    # Checks if graph is redundant
    lst = list(int(i) for i in y)
    if sum(lst) == 0:
        return None
            
    # Sets graph scale and creates model
    if log_boo_y and log_boo_x:
        plot = figure(title = title, tools = tools, tooltips = tooltips, sizing_mode = 'scale_width', plot_height=500, x_axis_type = 'log', y_axis_type = 'log')
    elif log_boo_x:
        plot = figure(title = title, tools = tools, tooltips = tooltips, 
            sizing_mode='scale_width', plot_height=500,
            x_axis_type = 'log')
    elif log_boo_y:
        plot = figure(title = title, tools = tools, tooltips = tooltips, y_axis_type = 'log',         sizing_mode = 'scale_width', plot_height = 500)
    else:
        plot = figure(title = title, tools = tools, tooltips = tooltips, 
            sizing_mode = 'scale_width', plot_height = 500)               
    
    # Creates Bokeh glyph   
    plot.line(x, y, color = 'navy')
    
    plot.hover.mode = 'vline'
    plot.xaxis.axis_label = 'Energy (keV)'
    plot.yaxis.axis_label = 'Cross Section (cm^2/g)'
    return plot
