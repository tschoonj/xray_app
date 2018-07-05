"""debug mode means server doesn't need to be restarted every time
alternatively: have app.run(debug=True)"""

from xray_app import app
        
if __name__ == '__main__':
        app.run()
