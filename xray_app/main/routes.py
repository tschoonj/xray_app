from flask import Blueprint, render_template, url_for
from xray_app.main.plot import TestClass 

main = Blueprint('main', __name__)

@main.route("/about")
def about():
        return render_template('about.html', title = 'About ')
        
@main.route("/plot")
def plot():
        return render_template('plot.html', title = 'Plot')
  
