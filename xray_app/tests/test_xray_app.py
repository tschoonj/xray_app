import pytest
import xraylib
import sys
import flask
from bs4 import BeautifulSoup

sys.path.insert(0, '..')
app = flask.Flask(__name__)

import xray_app

@pytest.fixture
def client():
	client = xray_app.app.test_client()
	yield client

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

#def test_soup(client):
#	rv = client.get('/')
#	soup = BeautifulSoup(rv.data, 'html.parser')
#	print(soup)
#	print(soup.find(id="output"))

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

#could possibly make an if function with valid input test and it loops
#test failures would be harder to find though

class BaseTest():
	def __init__(self): 
		self.status = 'assert 200 == rv.status_code'
		self.test_input = {
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
	def print_text(self):
		print(self.text)
 
class ValidInputTests(BaseTest):
	def __init__(self):
		BaseTest.__init__(self)
		self.text = 'This is a valid input test'	

class InvalidInputTests(BaseTest):
        def __init__(self):
                BaseTest.__init__(self)
                self.text = 'This is an invalid input test'

class TestFactory(object):
	@staticmethod
	def new_test(test_type):
		if test_type == 'ValidInput':
			return ValidInputTests()
		elif test_type == 'InvalidInput':
			return InvalidInputTests()
		else:
			print('Test Type does not exist')

FUNCTION_TYPES = ['ValidInput', 'InvalidInput']
FUNCTION_TESTS = []

for function in FUNCTION_TYPES:
	FUNCTION_TESTS.append(TestFactory().new_test(function))

for i in FUNCTION_TESTS:
	i.print_text() 

def test_atomicweight_with_valid_input(client):
	test_input.update({'function':'AtomicWeight', 'int_z':'5'})
	rv = client.post('/', data=test_input)
	val = xraylib.AtomicWeight(5)
	soup = BeautifulSoup(rv.data, 'html.parser')
	output = float(soup.find('div', id='output').string)
	print(output)
	assert 200 == rv.status_code
	assert b'g mol<sup>-1</sup>' in rv.data
	assert output == pytest.approx(val)

def test_atomicweight_with_invalid_input_int(client):
	test_input.update({'function':'AtomicWeight', 'int_z':'0'})
	rv = client.post('/', data=test_input)
	assert 200 == rv.status_code
	assert b'Invalid input' in rv.data

def test_atomicweight_with_invalid_input_str(client):
	test_input.update({'function':'AtomicWeight', 'int_z':'a'})
	rv = client.post('/', data=test_input)
	assert 200 == rv.status_code
	assert b'Invalid input' in rv.data

def test_elementdensity_with_valid_input(client):
	test_input.update({'function':'ElementDensity', 'int_z':'5'})
	rv = client.post('/', data=test_input)
	assert 200 == rv.status_code
	#assert xlib data present
	assert b'g cm<sup>-3</sup>' in rv.data

def test_elementdensity_with_invalid_input_str(client):
        test_input.update({'function':'ElementDensity', 'int_z':'a'})
        rv = client.post('/', data=test_input)
        assert 200 == rv.status_code
        #assert xlib data present
        assert b'Invalid input' in rv.data

def test_elementdensity_with_invalid_input_int(client):
        test_input.update({'function':'ElementDensity', 'int_z':'0'})
        rv = client.post('/', data=test_input)
        assert 200 == rv.status_code
        #assert xlib data present
        assert b'Invalid input' in rv.data

#FF_Rayl and RadNuc
