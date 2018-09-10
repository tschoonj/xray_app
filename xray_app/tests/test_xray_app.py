import pytest
import xraylib
import sys
import flask

from bs4 import BeautifulSoup

sys.path.insert(0, '..')
app = flask.Flask(__name__)

import xray_app
from xray_app.methods.utils import calc_output, check_xraylib_key, validate_str, validate_int, validate_float

@pytest.fixture
def client():
	client = xray_app.app.test_client()
	yield client
#----------------------------------------------------------------------------	
test_input = {
	'comp': '', 'int_z':'',	'int_z_or_comp': '', 'float_q': '',	
	'transition-notation': '', 'transition-iupac1':'',
	'transition-iupac2':'', 'transition-siegbahn':'', 
	'shell': '', 'energy': '', 'theta': '', 'phi': '', 
	'density': '','pz': '', 'cktrans': '', 
	'nistcomp': '', 'augtrans': '', 'rad_nuc': '', 
	'augtrans-ex_shell' : '', 'augtrans-trans_shell': '', 'augtrans-aug_shell':''} 

trans_functions = ['LineEnergy', 'RadRate', 
    'CS_FluorLine', 'CS_FluorLine_Kissel_Cascade',
    'CS_FluorLine_Kissel_Nonradiative_Cascade',
    'CS_FluorLine_Kissel_Radiative_Cascade']

test_z = ['26', '0', '-1', 'Fe', ' ']
test_q = ['0.5', '0', '-1', ' ']
test_z_comp = ['26', '0', '-1', 'Fe', 'FeSO4', ' ']
test_energy = ['10.5', '-1', ' ']
test_angle = ['1.5', '0', '-1', ' ']
test_comp = ['FeSO4', '0', '-1', ' ', '0.5']
test_pz = ['1.5', '0', '-1', ' ']
test_density = ['1.5', '0', '-1', ' ']
test_shell = ['K_SHELL']
test_cktrans = ['FL12_TRANS']

test_notation = ['IUPAC', 'Siegbahn']
test_siegbahn = ['KA1_LINE']
test_iupac1 = ['K']
test_iupac2 = ['L3']

test_ex_shell = ['K']
test_trans_shell = ['L1']
test_aug_shell = ['L1']    
#----------------------------------------------------------------------------
def vanilla_test(client, rv):
    assert 200 == rv.status_code
    assert b"rel=\"stylesheet\""
    assert b"type=\"text/css\""
    assert b"href=\"/static/style.css\""
    
def invalid_input_test(rv):
    assert 200 == rv.status_code
    #print(rv.data)
    assert b'Please enter valid input.' in rv.data
    print('Invalid Input Tested')

def output_test(rv, function, *values):    
    values = [i for i in values]
    print('calc output values' + str(values))
    if 'IUPAC' in values:
        if function.startswith('CS_FluorLine'):
            # Reorder input to Z, trans, E            
            trans = values[3] + values[4] + '_LINE'
            values.append(trans)
            order = [0, -1, 1]
            values = [values[i] for i in order]

        else:
            # Stitches trans together
            trans = values[2] + values[3] + '_LINE'
            values.append(trans)
            # Removes extraneous input
            order = [0, -1] 
            values = [values[i] for i in order]
            print(values)

    elif 'Siegbahn' in values:
        print(values)
        if function.startswith('CS_FluorLine'):
            order = [0, -1, 1]
            values = [values[i] for i in order]            

        else:
            order = [0, -1]
            values = [values[i] for i in order] 
 
    elif function == 'AugerRate':
        augtrans = values[1] + '_' + values[2] +values[3] + '_AUGER'
        values.append(augtrans)
        order = [0, -1]
        values = [values[i] for i in order]       
    else:
        val = calc_output(function, *values)        
        
    val = calc_output(function, *values)
    # calc_output gives 0 as a string
    # .approx() does not take str input
    if val == '0':
        val = 0
    output = soup_output(rv)
    assert 200 == rv.status_code
    assert output == pytest.approx(val)
    
# Note: order of variables needs to be the same as for method
def function_test(client, select_input, **variables):
    # - character forbidden for kwargs
    if select_input in trans_functions:
        variables['transition-notation'] = test_notation
        variables['transition-iupac1'] = test_iupac1
        variables['transition-iupac2'] = test_iupac2
        variables['transition-siegbahn'] = test_siegbahn
    if select_input == 'AugerRate':    
        variables['augtrans-ex_shell'] = test_ex_shell
        variables['augtrans-trans_shell'] = test_trans_shell
        variables['augtrans-aug_shell'] =  test_aug_shell

    test_inputs = []
    lst = [[]]
    print(lst)
    test_values = [variables[k] for k in variables] 
        
    # Generates list of all possible permutations of test variables
    for test_value in test_values:
        lst = [i + [value] for i in lst for value in test_value]    
    
    # Turn list of lists of permutations into lists of dicts of permutations
    for values in lst:
        _input = (list(values))
        test_dict = (dict(zip(variables.keys(), _input)))        
        test_inputs.append(test_dict)                
    
    # Each test dict is used as a mock request        
    for i in test_inputs:
        function_input = dict(test_input, function = select_input)        
        function_input.update(i)
        print('function input /n')
        print(function_input)
        rv = client.post('/', data = function_input)
        if validate_input(i):
            print("testing valid")
            output_test(rv, select_input, *list(i.values()))
        else:
            invalid_input_test(rv) 
            
"""def example_test(rv, select_input, *args):
    print('example test')
    print(args)
  """                    
#----------------------------------------------------------------------------    
def validate_input(dct):
    values = list(dct.values())    
    boo_list = [validate_int(value) or check_xraylib_key(value) or validate_str(value) or validate_float(value) for value in values]
    # Validating int and float allows int_z : 0 to fall through as True
    if 'int_z' in dct and dct['int_z'] == '0':
        return False
    elif 'int_z_or_comp' in dct and dct['int_z_or_comp'] == '0':
        return False
    print(dct.items())
    print(boo_list)
    return all(boo_list)

def soup_output(rv):
    soup = BeautifulSoup(rv.data, 'html.parser')
    #print(soup.prettify())
    output = soup.find('p', id="output").string
    output = float(output.replace(" ",""))
    return output

def soup_output_table(rv):
    soup = BeautifulSoup(rv.data, 'html.parser')
    #print(soup)
    #return output
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
    for x in test_functions:
        function_test(client, x, int_z = test_z)    

def test_ffrayl_sfcompt(client):
    test_functions = ['FF_Rayl', 'SF_Compt']
    for x in test_functions:
        function_test(client, x, int_z = test_z, float_q = test_q)
#----------------------------------------------------------------------------
def test_lineenergy_radrate(client):
    test_functions = ['LineEnergy', 'RadRate']
    for x in test_functions:
        function_test(client, x, int_z = test_z)
    #add test for all
    
def test_fluorline(client):
    test_functions = ['CS_FluorLine', 'CS_FluorLine_Kissel_Cascade', 'CS_FluorLine_Kissel_Nonradiative_Cascade', 'CS_FluorLine_Kissel_Radiative_Cascade']
    for x in test_functions:
        function_test(client, x, int_z = test_z, energy = test_energy)      
#----------------------------------------------------------------------------
def test_edgeenergy_etc(client):
    test_functions = ['EdgeEnergy', 'JumpFactor', 'FluorYield', 'AugerYield', 'AtomicLevelWidth', 'ElectronConfig']
    for x in test_functions:
        function_test(client, x, int_z = test_z, shell = test_shell)

def test_augerrate(client):
    function_test(client, 'AugerRate', int_z = test_z) 
#----------------------------------------------------------------------------
def test_cs(client):
    test_functions = ['CS_Total', 'CS_Photo', 'CS_Rayl', 'CS_Compt', 'CS_Energy']
    for x in test_functions:
        function_test(client, x, int_z_or_comp = test_z_comp, energy = test_energy)
       
def test_cs_kn(client):
    function_test(client, 'CS_KN', energy = test_energy)

def test_cs_photo_partial(client):
    function_test(client, 'CS_Photo_Partial', int_z = test_z, shell = test_shell, energy = test_energy)        
#----------------------------------------------------------------------------
def test_dcs(client):
    test_functions = ['DCS_Rayl', 'DCS_Compt']
    for _function in test_functions:
        function_test(client, _function, int_z_or_comp = test_z_comp, energy = test_energy, theta = test_angle)        

def test_dcs_kn_compt(client):
    test_functions = ['DCS_KN', 'ComptonEnergy']
    for x in test_functions:
        function_test(client, x, energy = test_energy, theta = test_angle)

def test_dcs_thoms(client):
    function_test(client, 'DCS_Thoms', theta = test_angle)
#----------------------------------------------------------------------------        
def test_dcsp(client):
    test_functions = ['DCSP_Rayl', 'DCSP_Compt']
    for x in test_functions:
        function_test(client, x, int_z_or_comp = test_z_comp, energy = test_energy, theta = test_angle, phi = test_angle)

def test_dcsp_thoms(client):
    function_test(client, 'DCSP_Thoms', theta = test_angle, phi = test_angle)

def test_dcsp_kn(client):
    function_test(client, 'DCSP_KN', energy = test_energy, theta = test_angle, phi = test_angle)
#----------------------------------------------------------------------------        
def test_fi_fii(client):
    test_functions = ['Fi', 'Fii']
    for x in test_functions:
        function_test(client, x, int_z = test_z, energy = test_energy)

def test_cktransprob(client):
    function_test(client, 'CosKronTransProb', int_z = test_z, cktrans = test_cktrans)

def test_comptprof(client):
    function_test(client, 'ComptonProfile', int_z = test_z, pz = test_pz)
    
def test_comptprof_part(client):
    function_test(client, 'ComptonProfile_Partial', int_z = test_z, shell = test_shell, pz = test_pz)

def test_mom_trans(client):
    function_test(client, 'MomentTransf', energy = test_energy, theta = test_angle)

#system error
#def test_c_parser(client):
    #function_test(client, 'CompoundParser', comp = test_comp)
"""
def test_get_by_ind(client):
    pass
        
def test_get_list(client):
    pass
def test_ref_ind(client):
    function_test(client, 'Refractive_Index', int_z_or_comp = test_z_comp, energy = test_energy, density = test_density)
    """
