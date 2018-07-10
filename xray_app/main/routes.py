from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def index():
        return render_template('index.html') 
        
@main.route("/about")
def about():
        return render_template('about.html', title = 'About Us:')
        
@main.route("/plot")
def plot():
        return render_template('plot.html', title = 'Plot')
  
#url_for('static', filename='style.css')
