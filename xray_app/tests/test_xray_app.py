import pytest
import xraylib
import sys

sys.path.insert(0, '..')

import xray_app


@pytest.fixture
def client():
	client = xray_app.app.test_client()

	yield client

def test_atomicweight_nonexistent(client):
	rv = client.get('/atomicweight_nonexistent')
	#for key in rv.__dict__:
	#print(f'{key} -> {rv.__dict__[key]}')
	assert 404 == rv.status_code

def test_atomicweight_vanilla(client):
	rv = client.get('/atomicweight')
	assert 200 == rv.status_code
	assert b'<h2> Result: </h2>\n\n\n      </div>' in rv.data
	assert b'<input type="text" name="atm_num"> <br>' in rv.data

def test_atomicweight_with_valid_input(client):
	rv = client.post('/atomicweight', data=dict(atm_num=5))
	assert 200 == rv.status_code
	assert b'<input type="text" name="atm_num" value=5>' in rv.data
	assert b'<h2> Result: </h2>\n\n10.81\n\n\n' in rv.data
	
