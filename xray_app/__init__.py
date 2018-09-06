from flask import Flask, url_for

app=Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f8463221fsg654dfhsh45'

# Import blueprint instances
from xray_app.methods.routes import methods
from xray_app.main.routes import main

app.register_blueprint(methods)
app.register_blueprint(main)
