from flask import Blueprint, render_template, request, url_for, make_response
from xray_app.main.forms import Xraylib_Request_Plot

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import xraylib

from xray_app.methods.routes import cs_tup

main = Blueprint('main', __name__)

@main.route("/about")
def about():
    return render_template('about.html', title = 'About ')

@main.route("/plot/fig.png")
def fig():
    pass
    
    
    #return png_output.getvalue()
    #canvas.print_png(png_output.getvalue()) #THIS IS THE PROBLEM
    #response=make_response(png_output.getvalue())
    #response.headers['Content-Type'] = 'image/png'
    #return response

@main.route("/plot", methods=['GET', 'POST'])
def plot():
    form = Xraylib_Request_Plot()
    form.function.choices = form.function.choices + cs_tup
   
    if request.method == 'POST':        
        #for key in request.form.keys():
        #print(f'key= {key}')
                
        select_input = request.form.get('function')

        plot = make_plot(str(select_input), 'Element', 'Weight')
                  
        return render_template('plot.html', form = form, title = 'Plot', plot=plot)
                
    return render_template('plot.html', title = 'Plot', form = form)
  
def graph_data(function):   
    pass

def print_data(*lsts):
    lst = zip(*lsts)    
    for value in lst:
            print(value)
    
def make_plot(function, xaxis, yaxis):
    x = []
    y = [] 
    xrl_function = getattr(xraylib, function)
    for i in range(1, 20, 1):
            x.append(i)
            y.append(float(xrl_function(i)))
            
    fig = Figure()
    canvas = FigureCanvas(fig)
            
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(title = function, xlabel = xaxis, ylabel = yaxis)            
            
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img_bytes = img.getvalue()
    img.close()
    img64 = str(base64.b64encode(img_bytes), encoding='utf-8')
    return img64  
