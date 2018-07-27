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

#----------------------------------------------------------------------------
from abc import abstractmethod, ABC
import random

def main():
    vanilla_tests = give_me_tests(Test_VanillaFactory)
    print('{} vanilla tests'.format(len(vanilla_tests)))
    for vanilla_test in vanilla_tests:
        print_test(vanilla_test)

def print_test(test, show_repr=False, show_hierarchy=False ):
    print(str(test))
    if show_repr:
        print(repr(test))
    if show_hierarchy:
        print(inspect.getmro(test.__class__))
        print('\n')

def give_me_tests(factories, test_type=None):
    #interface between client and Factory class
    #factories list of factory classses or one
    #test_typ str passes to making method
    #returns a list of objects made by the Factory classes
    if not hasattr(factories, '__len__'):
        factories = [factories]
    products = list()
    for factory in factories:
        product = factory.make_test(test_type)
        products.append(product)
        
    return products

class TestFactory():
    #abstract factory class to make tests
    #must be subclassed by factory class that calls the tests method
    @classmethod
    @abstractmethod
    def products(cls):
        pass
    
    @classmethod
    @abstractmethod
    def make_test(cls, test_type=None):
        test_name = random.choice(cls.products())
        this_module = __import__(__name__)
        test_class = getattr(this_module, test_name)
        test = test_class(factory_name=cls.__name__)
        if test_type is not None:
            test.test_type = test_type
        return test   
    
    @classmethod
    @abstractmethod
    def test_type(cls):
        return 'vanilla'

class _Test(ABC):
    #base abstract class for tests.
    def __init__(self, factory_name=None):
        self._manufactured = factory_name
        self._test_type = 'vanilla'
    def __str__(self):
        return 'made by:{}, {}, test type: {}, testing: {}'.format(self.manufactured, self.__class__.__name__, self.test_type, self.test_page)
    
    @property
    @abstractmethod
    def test_page(self):
        pass
    
    @property
    def test_type(self):
        return self._test_type
    
    @test_type.setter
    def test_type(self, new_type):
        self._test_type = new_type
        
    @property
    def manufactured(self):
        return self._manufactured

    @manufactured.setter
    def manufactured(self, factory_name):
        self._manufactured = factory_name    
            
class Test_VanillaFactory(TestFactory):
    @classmethod
    @abstractmethod
    def products(cls):
        return tuple(['test_index', 'test_about', 'test_plot'])

class _Vanilla(_Test):
    #basic concrete class for vanilla tests
    @property
    def test_type(self):
        return 'Vanilla'
        
class test_index(_Vanilla):
    @property
    def test_page(self):
        return 'index'
        
class test_about(_Vanilla):
    @property
    def test_page(self):
        return 'about'

class test_plot(_Vanilla):
    @property
    def test_page(self):
        return 'plot'
    
        
class Test_InvalidFactory(TestFactory):
    @classmethod
    @abstractmethod
    def products(cls):
        return tuple(['_int_z', '_float_q', '_etc'])
        
if __name__ == '__main__':
    main()    
#----------------------------------------------------------------------------    
            
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
