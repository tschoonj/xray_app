import pytest
import xraylib
import sys
import flask

sys.path.insert(0, '..')
app = flask.Flask(__name__)

import xray_app
from xray_app import app

@pytest.fixture
def client():
	client = xray_app.app.test_client()
	yield client

def test_atomicweight_nonexistent(client):
	rv = client.get('/atomicweight_nonexistent')
	#for key in rv.__dict__:
	#	print(f'{key} -> {rv.__dict__[key]}')
	assert 404 == rv.status_code

def test_atomicweight_vanilla(client):
	rv = client.get('/atomicweight')
	assert 200 == rv.status_code
	assert b'<h2> Result: </h2>' in rv.data
	assert b'<input type = "text" name = "int_z">' in rv.data

with app.test_request_context('/?int_z=5'):
	assert flask.request.path == '/'
	assert flask.request.args['int_z'] == '5'

def test_atomicweight_with_valid_input(client):
	rv = client.post('/atomicweight', data=dict(int_z=5))
	assert 200 == rv.status_code
	assert b'<input type = "text" name = "int_z" value = 5>' in rv.data
	assert b'<h2> Result: </h2>\n\n10.81\n\n\n' in rv.data

def test_atomicweight_with_invalid_input_int(client):
	rv = client.post('/atomicweight', data=dict(int_z=0))
	assert 200 == rv.status_code
	assert b'<input type = "text" name = "int_z"' in rv.data
	assert b'Invalid input' in rv.data

def test_atomicweight_with_invalid_input_str(client):
        rv = client.post('/atomicweight', data=dict(int_z=''))
        assert 200 == rv.status_code
        assert b'<input type = "text" name = "int_z"' in rv.data
        assert b'Invalid input' in rv.data

