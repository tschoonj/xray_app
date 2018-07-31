from flask import Blueprint, render_template, request, url_for
from xray_app.main.forms import Xraylib_Request_Plot
from xray_app.methods.routes import cs_tup

main = Blueprint('main', __name__)

@main.route("/about")
def about():
        return render_template('about.html', title = 'About ')
        
@main.route("/plot")
def plot():
        form = Xraylib_Request_Plot()
        form.function.choices = form.function.choices + cs_tup
        if request.method == 'POST':        
               #for key in request.form.keys():
                   #print(f'key= {key}')
                
                select_input = request.form.get('function')
                int_z = request.form['int_z']
                float_q = request.form['float_q']
                comp = request.form['comp']
                int_z_or_comp = request.form['int_z_or_comp']
                energy = request.form['energy']
                theta = request.form['theta']
                phi = request.form['phi']
                density = request.form['density']
                pz = request.form['pz']
                
                return render_template('plot.html', title = 'Plot')
                
        return render_template('plot.html', title = 'Plot')
  
  
