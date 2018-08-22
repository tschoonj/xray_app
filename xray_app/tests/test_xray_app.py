import pytest
import xraylib
import sys
import flask

from bs4 import BeautifulSoup

sys.path.insert(0, '..')
app = flask.Flask(__name__)

import xray_app
from xray_app.methods.utils import calc_output, check_xraylib_key

@pytest.fixture
def client():
	client = xray_app.app.test_client()
	yield client    
#----------------------------------------------------------------------------
def vanilla_test(client, rv):
    assert 200 == rv.status_code
    assert b"rel=\"stylesheet\""
    assert b"type=\"text/css\""
    assert b"href=\"/static/style.css\""
    
def invalid_input_test(rv):
    assert 200 == rv.status_code
    assert b'Invalid input' or b'Error' in rv.data
    print('Invalid Input Tested')

def output_test(rv, function, *values):
    output = soup_output(rv)   
    val = calc_output(function, *values)
    #print('value:')
    print(val)   
    assert 200 == rv.status_code
    assert output == pytest.approx(val)
    
#note order of variables needs to be the same as if it were going into the function
def function_test(client, _function, **variables):    
    #print(variables)
    test_inputs = []
    test_values = [variables[k] for k in variables]
    result = [[]]
    
    for test_value in test_values:
        result = [i + [value] for i in result for value in test_value]    
    
    for values in result:
        _input = (list(values))
        test_dict = (dict(zip(variables.keys(), _input)))        
        test_inputs.append(test_dict)        
        
    for i in test_inputs:
        function_input = dict(test_input, function = _function)
        function_input.update(i)
        rv = client.post('/', data = function_input)
        #print(list(i.values()))
        if validate_input(i):
            output_test(rv, _function, *list(i.values()))
        else:
            invalid_input_test(rv)       
#----------------------------------------------------------------------------    
test_input = {
	'comp': '', 'int_z':'',	'int_z_or_comp': '', 'float_q': '',	'linetype-trans_notation': '', 'linetype-trans_iupac':'', 'linetype-trans_siegbahn':'', 'shell': '', 'energy': '', 'theta': '', 'phi': '', 'density': '','pz': '', 'cktrans': '', 'nistcomp': '', 'augtrans': '', 'rad_nuc': ''
    }

test_z = [26, 'Fe', ' ']
test_q = [0.5, ' ']
test_z_comp = [26, 'Fe', 'FeSO4', ' ']
test_energy = [10.0, ' ']
test_angle = [1.0, ' ']
test_comp = []
test_shell = ['K_SHELL']

def validate_input(dct):
    boo_list = [isinstance(value, (float, int)) or xraylib.SymbolToAtomicNumber(value) != 0 or check_xraylib_key(value) for value in list(dct.values())]
    #print(boo_list)
    if all(boo_list):
        return True
    else:
        return False

def soup_output(rv):
    soup = BeautifulSoup(rv.data, 'html.parser')
    #print(soup)
    output = soup.find('p', id="output").string
    output = float(output.replace(" ",""))
    return output   
#----------------------------------------------------------------------------                
def test_nonexistent(client):
	rv = client.get('/nonexistent')
	#for key in rv.__dict__:
	#	print(f'{key} -> {rv.__dict__[key]}')
	assert 404 == rv.status_code

def test_index_vanilla(client):
	rv = client.get('/')
	vanilla_test(client, rv)
	assert b'<div class="form-group" id="function">' in rv.data
	assert b'<option value="AtomicWeight">Atomic Weight</option>' in rv.data
	assert b'type="submit"' in rv.data

def test_plot_vanilla(client):
	rv = client.get('/plot')
	vanilla_test(client, rv)
	
def test_about_vanilla(client):
	rv = client.get('/about')
	vanilla_test(client, rv)              
#----------------------------------------------------------------------------                
def test_atomweight_elementdens(client): 
    test_functions = ['AtomicWeight', 'ElementDensity']
    for _function in test_functions:
        function_test(client, _function, int_z = test_z)    

def test_ffrayl_sfcompt(client):
    test_functions = ['FF_Rayl', 'SF_Compt']
    for _function in test_functions:
        function_test(client, _function, int_z = test_z, float_q = test_q)
#----------------------------------------------------------------------------
"""def test_lineenergy(client):
    test_z = [5, 'Fe', 'a']
    for value in test_z:
        function_input = dict(test_input, function = 'LineEnergy', int_z = value, linetype_trans_notation = 'IUPAC', linetype_trans_iupac = 'KL1_LINE')
        rv = client.post('/', data = function_input)
        if isinstance(value, int):
            output_test(client, rv, 'LineEnergy', value, xraylib.KL1_LINE)
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            output_test(client, rv, 'LineEnergy', value, xraylib.KL1_LINE)
        else:
            invalid_input_test(client, rv)
#methods req. linetype: LineEnergy, RadRate, CSFluorLines2"""
#----------------------------------------------------------------------------
# add in test for units
def test_edgeenergy_etc(client):
    test_functions = ['EdgeEnergy', 'JumpFactor', 'FluorYield', 'AugerYield', 'AtomicLevelWidth', 'ElectronConfig']
    for _function in test_functions:
        function_test(client, _function, int_z = test_z, shell = test_shell)

#All CS excl. PP and KN
def test_cs(client):
    test_functions = ['CS_Total', 'CS_Photo', 'CS_Rayl', 'CS_Compt', 'CS_Energy']
    for _function in test_functions:
        function_test(client, _function, int_z_or_comp = test_z_comp, energy = test_energy)
        
def test_cs_kn(client):
    function_test(client, 'CS_KN', energy = test_energy)

def test_cs_photo_partial(client):
    function_test(client, 'CS_Photo_Partial', int_z = test_z, shell = test_shell, energy = test_energy)    

def test_dcs(client):
    test_functions = ['DCS_Rayl', 'DCS_Compt']
    for _function in test_functions:
        function_test(client, _function, int_z_or_comp = test_z_comp, energy = test_energy, theta = test_angle)        

def test_dcs_kn_compt(client):
    test_functions = ['DCS_KN', 'ComptonEnergy']
    for _function in test_functions:
        function_test(client, _function, energy = test_energy, theta = test_angle)              
