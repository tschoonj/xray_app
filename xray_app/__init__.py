from flask import Flask
from xraylib import AtomicWeight

app=Flask(__name__)
# app.debug = True; from old flask
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f8463221fsg654dfhsh45'


from xray_app.methods.routes import methods
from xray_app.main.routes import main
#importing blueprint instances

app.register_blueprint(methods)
app.register_blueprint(main)
#to prevent loop these imports need to be here, do not move them
