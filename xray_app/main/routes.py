from flask import Blueprint, render_template, url_for

main = Blueprint('main', __name__)

@main.route("/about")
def about():
        return render_template('about.html', title = 'About ')
        
@main.route("/plot")
def plot():
        return render_template('plot.html', title = 'Plot')
  
#url_for('static', filename='style.css')
