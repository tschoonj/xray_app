from flask import Flask
from xraylib import AtomicWeight


app=Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f8463221fsg654dfhsh45'


from xray_app import routes
#to prevent loop this import needs to be here, do not move it
