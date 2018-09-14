from flask import Blueprint, render_template, request
from xray_app.main.forms import Xraylib_Request_Plot
from xray_app.main.plotting import create_fig
from xray_app.main.ptable import create_table
from xray_app.methods.utils import calc_output
from xray_app.methods.routes import cs_dict, trans_S_tup, trans_I_tup, make_tup, validate_int, validate_str, validate_float
from bokeh.embed import components

import xraylib

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
# About Page
@main.route("/about")
def about():
    return render_template('about.html', title = 'About ')
#---------------------------------------------------------------------------------
# Periodic Table Page
@main.route("/ptable")
def ptable():
    table = create_table()
    script, div = components(table)
    return render_template('ptable.html', title = 'Periodic Table', script=script, div=div)    
#---------------------------------------------------------------------------------
# Plotting interface
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
                if plot:
                    script, div = components(plot)
                    return render_template('plot.html', form = form, title = 'Plot', script = script, div = div)
                else:
                    return render_template('plot.html', form = form, title = 'Plot')
            else:
                return render_template('plot.html', form = form, title = 'Plot')
    
        elif select_input.startswith('CS_FluorLine'):
            if validate_int(int_z) or validate_str(int_z):
                if notation == 'IUPAC':
                    plot = create_fig(select_input, range_start, range_end, 
                            log_boo_x, log_boo_y, int_z, trans)
                    if plot:
                        script, div = components(plot)
                        return render_template('plot.html', form = form, title = 'Plot', script = script, div = div)
                    else:
                        return render_template('plot.html', form = form, title = 'Plot')    

                elif notation == 'Siegbahn':
                    plot = create_fig(select_input, range_start, range_end, 
                            log_boo_x, log_boo_y, int_z, siegbahn)
                    if plot:
                        script, div = components(plot)
                        return render_template('plot.html', form = form, title = 'Plot', script = script, div = div)
                    else:
                        return render_template('plot.html', form = form, title = 'Plot')
            else:
                return render_template('plot.html', form = form, title = 'Plot')
    return render_template('plot.html', title = 'Plot', form = form)

