import pytest
import xraylib
import sys
import flask
import random

from bs4 import BeautifulSoup

sys.path.insert(0, '..')
app = flask.Flask(__name__)

import xray_app
from xray_app.methods.utils import calc_output

@pytest.fixture
def client():
	client = xray_app.app.test_client()
	yield client    
#----------------------------------------------------------------------------
def vanilla_test(client, rv):
    assert 200 == rv.status_code
    
def invalid_input_test(client, rv):
    assert 200 == rv.status_code
    assert b'Invalid input' or b'Error' in rv.data
    print('Invalid Input Tested')

def output_test(client, rv, function, *value):
    output = soup_output(rv)
    val = calc_output(function, *value)   
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
    #print(soup)
    output = soup.find('div', id="output").string
    print(output)
    output = float(output.replace(" ",""))
    return output   
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
def function_test(client, xrl_function, *variables):
    for variable in variables:
        test_values = []
        if variable == 'int_z':
            test_values.append(5)
            test_values.append('Fe')
            test_values.append('a')
            print(test_values)
        if variable == 'float_q':
            test_values.append(0.5)
            test_values.append(0.5)
            test_values.append('a')
    for value in test_values:
        function_input = dict(test_input, function = xrl_function, int_z = value)
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            assert b'g cm<sup>-3</sup>' in rv.data
            output_test(client, rv, 'ElementDensity', value)
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            output_test(client, rv, 'ElementDensity', value)
        else:
            invalid_input_test(client, rv)     
    
#function_test(client, 'Rayl_FF', 'int_z', 'float_q')
#----------------------------------------------------------------------------                
def test_atomicweight(client):
    #function_test(client, 'AtomicWeight', test_input)
    int_z = [5, 'Fe', 'a']
    for value in int_z:
        function_input = dict(test_input, function = 'AtomicWeight', int_z = value)
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            assert b'g mol<sup>-1</sup>' in rv.data
            output_test(client, rv, 'AtomicWeight', value)
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            assert b'g mol<sup>-1</sup>' in rv.data
            output_test(client, rv, 'AtomicWeight', value)
        else:
            invalid_input_test(client, rv)
#----------------------------------------------------------------------------
def test_elementdensity(client):
    int_z = [5, 'Fe', 'a']
    for value in int_z:
        function_input = dict(test_input, function = 'ElementDensity', int_z = value)
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            assert b'g cm<sup>-3</sup>' in rv.data
            output_test(client, rv, 'ElementDensity', value)
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            assert b'g cm<sup>-3</sup>' in rv.data
            output_test(client, rv, 'ElementDensity', value)
        else:
            invalid_input_test(client, rv)        
#----------------------------------------------------------------------------                        
def test_ff_rayl(client):
    test_z = [5, 'Fe', 'a']
    for value in test_z:
        function_input = dict(test_input, function = 'FF_Rayl', int_z = value, float_q = 0.5)
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            output_test(client, rv, 'FF_Rayl', value, 0.5)
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            output_test(client, rv, 'FF_Rayl', value, 0.5)
        else:
            invalid_input_test(client, rv)
    
    test_q = [0.5, 'a']
    for value in test_q:
        function_input = dict(test_input, function = 'FF_Rayl', int_z = 5, float_q = value)
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            output_test(client, rv, 'FF_Rayl', 5, value)
        else:
            invalid_input_test(client, rv) 
#----------------------------------------------------------------------------
def test_sf_compt(client):
    test_z = [5, 'Fe', 'a']
    test_q = [0.5, 'a']
    for value in test_z:
        function_input = dict(test_input, function = 'SF_Compt', int_z = value, float_q = test_q[0])
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            output_test(client, rv, 'SF_Compt', value, 0.5)
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            output_test(client, rv, 'SF_Compt', value, 0.5)
        else:
            invalid_input_test(client, rv)
    for value in test_q:
        function_input = dict(test_input, function = 'SF_Compt', int_z = 5, float_q = value)
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            output_test(client, rv, 'SF_Compt', 5, value)
        else:
            invalid_input_test(client, rv) 
#----------------------------------------------------------------------------
"""def test_lineenergy(client):
    test_z = [5, 'Fe', 'a']
    for value in test_z:
        function_input = dict(test_input, function = 'LineEnergy', int_z = value, linetype-trans_notation = 'IUPAC', linetype-trans_iupac = 'KL1_LINE')
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            output_test(client, rv, 'LineEnergy', value, xraylib.KL1_LINE)
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            output_test(client, rv, 'LineEnergy', value, xraylib.KL1_LINE)
        else:
            invalid_input_test(client, rv)"""
#----------------------------------------------------------------------------
def test_(client):
    pass
#----------------------------------------------------------------------------
def test_(client):
    pass
