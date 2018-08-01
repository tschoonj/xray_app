from flask import Blueprint, render_template, request, url_for, make_response
from xray_app.main.forms import Xraylib_Request_Plot

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO

import xraylib

from xray_app.methods.routes import cs_tup

main = Blueprint('main', __name__)

@main.route("/about")
def about():
    return render_template('about.html', title = 'About ')

@main.route("/plot/fig.png")
def fig():

    
    x = []
    y = []

    def graph_data(function):   
        function = getattr(xraylib, function)
        for i in range(1, 20, 1):
            x.append(i)
            y.append(float(function(i)))

    def print_data(*lsts):
        lst = zip(*lsts)    
        for value in lst:
            print(value)
    
    def make_plot(function, *labels, dpi):
        pass
            
    graph_data('ElementDensity')
    fig = Figure()
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Fig 1')
    ax.set(xlabel='X', ylabel='Y')
    ax.legend()
    
    canvas = FigureCanvas(fig)
    fig.savefig('fig.png', dpi=80)
    
    png_output = BytesIO()
    print(png_output.getvalue())
    print(canvas.print_png)
    canvas.print_png(png_output)
    #return png_output.getvalue()
    #canvas.print_png(png_output.getvalue()) #THIS IS THE PROBLEM
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@main.route("/plot", methods=['GET', 'POST'])
def plot():
    form = Xraylib_Request_Plot()
    form.function.choices = form.function.choices + cs_tup
    """import matplotlib.pyplot as plt
    from io import BytesIO
    
    x = []
    y = []

    def graph_data():   
        for i in range(1, 20, 1):
            x.append(i)
            y.append(xraylib.ElementDensity(i)) #change to elementdensity

    def print_data(*lsts):
        lst = zip(*lsts)    
        for value in lst:
            print(value)
            
    graph_data()
    fig = Figure()
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Fig 1')
    ax.set(xlabel='X', ylabel='Y')
    ax.legend()
    
    canvas = FigureCanvas(fig)
    fig.savefig('fig.png', dpi=80)
    
    png_output = BytesIO()
    print(png_output.getvalue())
    print(canvas.print_png)
    canvas.print_png(png_output)
    #return png_output.getvalue()
    #canvas.print_png(png_output.getvalue()) #THIS IS THE PROBLEM
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response   """   
    
    if request.method == 'POST':        
        #for key in request.form.keys():
        #print(f'key= {key}')
                
        select_input = request.form.get('function')
        
                
        return render_template('plot.html', form = form, title = 'Plot')
                
    return render_template('plot.html', title = 'Plot', form = form)
  
  
