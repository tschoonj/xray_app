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
    print('Invalid Input Tested')

def output_test(client, rv, function, *value):
    output = soup_output(rv)
    print(output)
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
    output = soup.find('div', id="output").string
    output = float(output.replace(" ",""))
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

def test_plot_vanilla(client):
	rv = client.get('/plot')
	vanilla_test(client, rv)
	
def test_about_vanilla(client):
	rv = client.get('/about')
	vanilla_test(client, rv)

#----------------------------------------------------------------------------                
"""def function_test(client, function, **values):
    #for function in xraylib:
    function_input = dict(test_input, function = str(function), **values)
    rv = client.post('/', data = function_input)
    print(**values)
    output_test(client, rv, function)"""

def test_atomicweight(client):
    #function_test(client, 'AtomicWeight', test_input)
    function_input = dict(test_input, function = 'AtomicWeight', int_z = '5')
    rv = client.post('/', data = function_input)
    output_test(client, rv, 'AtomicWeight', 5)
    assert b'g mol<sup>-1</sup>' in rv.data
     
    function_input = dict(test_input, function = 'AtomicWeight', int_z = 'a')
    rv = client.post('/', data = function_input)
    invalid_input_test(client, rv)
#----------------------------------------------------------------------------
def test_elementdensity(client):
    function_input = dict(test_input, function = 'ElementDensity', int_z = '5')
    rv = client.post('/', data = function_input)
    output_test(client, rv, 'ElementDensity', 5)
    assert b'g cm<sup>-3</sup>' in rv.data

    function_input = dict(test_input, function = 'ElementDensity', int_z = 'a')
    rv = client.post('/', data = function_input)
    invalid_input_test(client, rv)
#----------------------------------------------------------------------------                        
def test_ff_rayl(client):
    function_input = dict(test_input, function = 'FF_Rayl', int_z = '5', float_q = '0.5')
    rv = client.post('/', data = function_input)
    output_test(client, rv, 'FF_Rayl', 5, 0.5)

    function_input = dict(test_input, function = 'FF_Rayl', int_z = 'a', float_q = '0.5')
    rv = client.post('/', data = function_input)
    invalid_input_test(client, rv)

    function_input = dict(test_input, function = 'FF_Rayl', int_z = '5', float_q = 'a')
    rv = client.post('/', data = function_input)
    invalid_input_test(client, rv)
#----------------------------------------------------------------------------
def test_(client):
    pass
