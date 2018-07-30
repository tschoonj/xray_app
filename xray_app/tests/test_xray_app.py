import pytest
import xraylib
import sys
import flask
import random

from abc import abstractmethod, ABC
from bs4 import BeautifulSoup

sys.path.insert(0, '..')
app = flask.Flask(__name__)

import xray_app

@pytest.fixture
def client():
	client = xray_app.app.test_client()
	yield client

    
#----------------------------------------------------------------------------
def vanilla_test(client, rv):
    assert 200 == rv.status_code
    
def invalid_input_test(client, rv):
    assert 200 == rv.status_code
    assert b'Invalid input' in rv.data

def function_test(client, rv, function, *value):
    test_input[str(function)] = 'function'
    global output
    output = soup_output(rv)
    output = float(output.replace(" ",""))
    print(output)
    global val #global does not seem like a great solution
    val = calc_val(function, *value)   
    assert 200 == rv.status_code
    assert output == pytest.approx(val)
    #return output
    #return val
#----------------------------------------------------------------------------    
test_input = {
	'comp': '', 
	'int_z':'',
	'int_z_or_comp': '',
	'float_q': '',
	'linetype': '',
	'shell': '',
	'energy': '',
	'theta': '',
	'phi': '',
	'density': '',
	'pz': '',
	'cktrans': '',
	'nistcomp': '',
	'augtrans': '',
	'rad_nuc': ''
	}

def soup_output(rv):
    soup = BeautifulSoup(rv.data, 'html.parser')
    output = soup.find('div', id='output').string
    return output 

def calc_val(function, *value):
    function = getattr(xraylib, function)
    val = float(function(*value))
    return val
    

#----------------------------------------------------------------------------                

def test_nonexistent(client):
	rv = client.get('/nonexistent')
	#for key in rv.__dict__:
	#	print(f'{key} -> {rv.__dict__[key]}')
	assert 404 == rv.status_code

def test_style(client):
	rv = client.get('/')
	vanilla_test(client, rv)
	assert b"rel=\"stylesheet\""
	assert b"type=\"text/css\""
	assert b"href=\"/static/style.css\""

def test_navbar(client):
	pass

def test_js_present(client):
	rv = client.get('/')
	vanilla_test(client, rv)
	assert b"src=\"/static/main.js\""

def test_index_vanilla(client):
	rv = client.get('/')
	vanilla_test(client, rv)
	assert b'<div class = "form-group xlib" id = "comp">' in rv.data
	assert b'<option value="AtomicWeight">Atomic Weight</option>' in rv.data
	assert b'type = "submit"' in rv.data

def test_plots_vanilla(client):
	rv = client.get('/plot')
	vanilla_test(client, rv)
	
def test_about_vanilla(client):
	rv = client.get('/about')
	vanilla_test(client, rv)

#----------------------------------------------------------------------------                

def test_atomicweight(client):
    try:
        test_input.update({'function':'AtomicWeight', 'int_z':'5'})
        rv = client.post('/', data=test_input)
        function_test(client, rv, 'AtomicWeight', 5)
        assert b'g mol<sup>-1</sup>' in rv.data
    except ValueError:
        print("Valid Test Failed: Value Error")
    except TypeError:
        print("Test Failed: Type Error")
        
    try:
        test_input.update({'function':'AtomicWeight', 'int_z':'0'})
        rv = client.post('/', data=test_input)
        invalid_input_test(client, rv)
    except:
        print("Invalid Value Error")
        
    try:
        test_input.update({'function':'AtomicWeight', 'int_z':'a'})
        rv = client.post('/', data=test_input)
        invalid_input_test(client, rv)
    except:
        print("Invalid Type Error")
    #do try/except loop
    #try funct(val, inval)
    #except ValueError "testfailed " and TypeError

def test_elementdensity(client):
    try:
        test_input.update({'function':'ElementDensity', 'int_z':'5'})
        rv = client.post('/', data=test_input)
        function_test(client, rv, 'ElementDensity', 5)
        
        assert b'g cm<sup>-3</sup>' in rv.data
    except ValueError:
        print("Valid Test Failed: Value Error")
    except TypeError:
        print("Test Failed: Type Error")
        
    try:
        test_input.update({'function':'ElementDensity', 'int_z':'0'})
        rv = client.post('/', data=test_input)
        invalid_input_test(client, rv)
    except:
        print("Invalid Value Error")
        
    try:
        test_input.update({'function':'ElementDensity', 'int_z':'a'})
        rv = client.post('/', data=test_input)
        invalid_input_test(client, rv)
    except:
        print("Invalid Type Error")

#FF_Rayl and RadNuc
