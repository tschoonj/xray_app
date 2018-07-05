from flask import Flask
from xraylib import AtomicWeight


app=Flask(__name__)
app.debug = True
#app.config necessary for xraylib?

from xray_app import routes
#to prevent loop this import needs to be here, do not move it
