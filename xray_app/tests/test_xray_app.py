import pytest
import xraylib
import sys
import flask

sys.path.insert(0, '..')
app = flask.Flask(__name__)

import xray_app

@pytest.fixture
def client():
	client = xray_app.app.test_client()
	yield client

test_input = {
	'comp': '', 
	'int_z':'5',
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
def test_nonexistent(client):
	rv = client.get('/nonexistent')
	#for key in rv.__dict__:
	#	print(f'{key} -> {rv.__dict__[key]}')
	assert 404 == rv.status_code

def test_style(client):
	rv = client.get('/')
	assert 200 == rv.status_code
	assert b"rel=\"stylesheet\""
	assert b"type=\"text/css\""
	assert b"href=\"/static/style.css\""

def test_navbar(client):
	pass

def test_js_present(client):
	rv = client.get('/')
	assert 200 == rv.status_code
	assert b"src=\"/static/main.js\""

def test_index_vanilla(client):
	rv = client.get('/')
	assert 200 == rv.status_code
	assert b'<div class = "form-group xlib" id = "comp">' in rv.data
	assert b'<option value="AtomicWeight">Atomic Weight</option>' in rv.data
	assert b'type = "submit"' in rv.data

def test_plots_vanilla(client):
	rv = client.get('/')
	assert 200 == rv.status_code
	
def test_about_vanilla(client):
	rv = client.get('/about')
	assert 200 == rv.status_code

def test_atomicweight_with_valid_input(client):
	test_input['function']='AtomicWeight'
	rv = client.post('/', data=test_input)
	assert 200 == rv.status_code
	assert b'10.81' in rv.data
	assert b'g mol<sup>-1</sup>' in rv.data

def test_atomicweight_with_invalid_input_int(client):
	test_input.update({'function':'AtomicWeight', 'int_z':'0'})
	rv = client.post('/', data=test_input)
	assert 200 == rv.status_code
	assert b'Invalid input' in rv.data

def test_atomicweight_with_invalid_input_str(client):
	test_input.update({'function':'AtomicWeight', 'int_z':''})
	rv = client.post('/', data=test_input)
	assert 200 == rv.status_code
	assert b'Invalid input' in rv.data

