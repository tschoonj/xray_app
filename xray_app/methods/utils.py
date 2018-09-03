import xraylib

from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

#validators for input
def validate_float(*s):
    boo = []
    for i in s:
        try: 
            if float(i) >= 0:
                boo.append(True)
            else:
                boo.append(False)   
        except ValueError:
            return False
    return all(boo)

def validate_int(*s):
    boo = []
    for i in s:
        try:
            if float(i) == int(i) and int(i) > 0:
                boo.append(True)
            else:
                boo.append(False)              
        except:
            return False    
    return all(boo)    
                
def validate_str(*s):
    boo = []
    for i in s:
        try:                
            if xraylib.SymbolToAtomicNumber(i) != 0:
                boo.append(True)
            elif xraylib.CompoundParser(i):                    
                boo.append(True)
            else:
                boo.append(False)
        except:
            return False
    return all(boo)          
#------------------------------------------------------------------------------------------------
#generates dicts for all linetype output
def all_trans(tple, *inputs):
    transs = [x[0] for x in tple]
    output = {}    
    for trans in transs:
        out = calc_output(*inputs, trans)
        if out != 0:
            output[trans] = out       
    return output                   

#special case needed for xrf due to order of method input
def all_trans_xrf(tple, function, int_z, energy):
    transs = [x[0] for x in tple]
    output = {}
    for trans in transs:
        out = calc_output(function, int_z, trans, energy)
        if out != 0:
            output[trans] = out
    return output
#------------------------------------------------------------------------------------------------
#generates tuples from dicts after mapping 'user-friendly' strings onto the keys
def make_tup(_dict, variable):
    tup = []
    if variable == 'ck':
        tup = [(k, k.split('_')[0]) for k, v in _dict.items()]
        return tup
    elif variable == 'nist' or variable == 'rad':
        tup = [(k, k) for k, v in _dict.items()]
        return tup
    elif variable == 'cs' or variable == 'dcs':
        for k, v in _dict.items():
            split_k = k.split('_')
            k_label = []
            for word in split_k:
                if word in label_dict:
                    k_label.append(label_dict[word])
                else:
                    k_label.append(word)
            k_label = ' '.join(k_label)
            tpl = (k, k_label)
            tup.append(tpl)
        return tup
    else:
        for k, v in _dict.items():    
            split_k = k.split('_')
            k_label = split_k[0]
            tpl = (k, k_label)
            tup.append(tpl)
        return tup
        
#need to match each substr to dict key then 'translate' it        
label_dict = {'CS':'Cross Section:', 'DCS':'Differential Unpolarized Cross Section:', 'DCSP':'Differential Polarized Cross Section:', 'KN':'Klein-Nishina', 'Photo':'Photoionization', 'Rayl':'Rayleigh', 'Compt':'Compton', 'FluorLine':' XRF', 'Partial':'(Partial)', 'Thoms':'Thomson', 'TRANS':''}

#checks input for xrl keys also including transtion notation types
def check_xraylib_key(s):
        s = s.upper()
        s = s.replace(" ", "_")
        s = s.replace("-", "_")
        #print(s)
        for key in xraylib.__dict__.keys():
            #print (key)
            if s == key:
                #print('KEY FOUND')
                return True
            elif s == 'IUPAC' or s == 'SIEGBAHN':
                return True
            elif key.endswith('_' + s) and key.startswith('NIST'):
                #print('KEY FOUND') 
                return True
            elif key.endswith('_' + s) and key.startswith('RADIO'):
                #print('KEY FOUND') 
                return True
        return False

#user choice != xrl keys hence:              
def get_key(s):
    s = s.upper()
    s = s.replace(" ", "_")
    s = s.replace("-", "_")
    for key in xraylib.__dict__.keys():
            #print (key)
            if s == key:
                return key
            elif key.endswith('_' + s) and key.startswith('NIST'):
                return key
            elif key.endswith('_' + s) and key.startswith('RADIO'):
                return key

#calculates output for all functions excl. CompoundParser and Refractive_Index
def calc_output(function, *values):
    xrl_function = getattr(xraylib, function)
    print(values)

    lst = []
    for value in values:        
        if validate_int(value):
            lst.append(int(value))
        elif validate_float(value):
            lst.append(float(value))   
        elif check_xraylib_key(value):
            value = get_key(value)
            value = getattr(xraylib, value)
            lst.append(value)
        elif validate_str(value):
            if xraylib.SymbolToAtomicNumber(value) != 0:
                lst.append(xraylib.SymbolToAtomicNumber(value))
            else:
                lst.append(value) #needed for _CP entry         
    print(lst)
    try:
        if validate_float(lst[0]):
            output = xrl_function(*lst)
            print(output)
            if output == 0:
                #0 not truthy so jinja ignores it
                return '0'
            else:
                return output
        else: 
            xrl_function = getattr(xraylib, function + '_CP')
            output = xrl_function(*lst)
            print(output)
            if output == 0:
                return '0'
            else:
                return output
    except:
        output = 'Error'
        return output

#generates code example strings and passes them through Pygments
def code_example(tple, function, *variables):
    
    languages = [x[0] for x in tple]
    labels = [x[1] for x in tple]
    examples = []       
        
    for i in tple:
        lang = [i[0], i[1]] #could be done with list comprehension?
        lst = []
        #startinline arg lets php lexer highlight without prepending str with <?php
        lexer = get_lexer_by_name(lang[0], startinline=True)
        
        if lang[1] == 'C/C++/Objective-C':
            string = '#include <xraylib.h>'
            # &lt = < &gt = >
        elif lang[1] == 'Fortran 2003/2008':
            string = 'use :: xraylib'
        elif lang[1] == 'Perl':
            string = 'use xraylib.pm;'
        elif lang[1] == 'IDL':
            string = '@xraylib'
        elif lang[1] == 'Python':
            string = 'import xraylib'     
        elif lang[1] == 'Java':
            string = 'import com.github.tschoonj.xraylib.*;'
        elif lang[1] == 'C#/.NET':
            string = 'using Science;'
        elif lang[1] == 'Lua':
            string = 'require("xraylib")'
        elif lang[1] == 'Ruby':
            string = 'require \'xraylib\''
        elif lang[1] == 'PHP':
            string = 'include("xraylib.php");'
        #div class included for CSS
        pre_support = '<div class="support-examples ' + str(lang[0]) + '">Enable support for xraylib in ' + str(lang[1]) + ' using: </div>'
        support_html = highlight(string, lexer, HtmlFormatter(cssclass = str(lang[0]) + ' support-examples'))        
        
        if lang[0] == 'cpp-objdump':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)):
                    lst.append(variable)
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')          
            _input = ', '.join(lst)
            example = str(function) + '(' + _input + ')'
        
        elif lang[0] == 'fortran':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append("'" + str(variable) + "'")
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('symboltoatomicnumber(\'' + variable + '\')')
                elif check_xraylib_key(str(variable)):
                    lst.append((variable).lower())
                elif validate_str(variable):
                    lst.append("'" + str(variable) + "'")                  
            _input = ', '.join(lst)
            example = str(function).lower() + '(' + _input + ')'
        
        elif lang[0] == 'perl':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib::SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)):
                    lst.append('$xraylib::' + variable)  
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')                  
            _input = ', '.join(lst)
            example = 'xraylib::' + str(function) + '(' + _input + ')'
        
        elif lang[0] == 'idl':
            lst = []
            for variable in variables:
                if validate_float(variable) or check_xraylib_key(str(variable)):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append("'" + str(variable) + "'")
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SYMBOLTOATOMICNUMBER(\'' + variable + '\')')
                elif validate_str(variable):
                    lst.append("'" + str(variable) + "'")                 
            _input = ', '.join(lst)
            example = str(function).upper() + '(' + _input + ')'
        
        elif lang[0] == 'python':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)):
                    lst.append('xraylib.' + variable)
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')               
            _input = ', '.join(lst)
            example = 'xraylib.' + str(function) + '(' + _input + ')'
        
        elif lang[0] == 'java':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)):
                    lst.append('Xraylib.' + variable)
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')               
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'
        
        elif lang[0] == 'csharp':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('XrayLib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)):
                    lst.append('XrayLib.' + variable)
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')                
            _input = ', '.join(lst)
            example = 'XrayLib.' + str(function) + '(' + _input + ')'
        
        elif lang[0] == 'lua':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)):
                    lst.append('xraylib.' + variable)
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')
            _input = ', '.join(lst)
            example = 'xraylib.' + str(function) + '(' + _input + ')'
        
        elif lang[0] == 'ruby':
            for variable in variables:
                if validate_float(variable):
                    lst.append(variable)
                elif function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)):
                    lst.append('Xraylib::' + variable) 
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')               
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'        
        
        elif lang[0] == 'php': 
            for variable in variables:
                if function == 'GetCompoundDataNISTByName' or function == 'GetRadioNuclideDataByName':
                    lst.append('"' + str(variable) + '"')
                elif validate_float(variable) or check_xraylib_key(str(variable)):
                    lst.append(variable)                
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SymbolToAtomicNumber("' + variable + '")')
                elif validate_str(variable):
                    lst.append('"' + str(variable) + '"')                
            _input = ', '.join(lst)
            example = str(function) + '(' + _input + ')'
        
        #div class included for CSS
        example_html = highlight(example, lexer, HtmlFormatter(cssclass = str(lang[0]) + ' code-examples'))
        pre_example = '<div class="code-examples ' + str(lang[0]) + '">Call as: </div>'
        #print(HtmlFormatter().get_style_defs('.' + str(lang[0]))) #prints css
               
        examples.append(pre_support)
        examples.append(support_html)
        examples.append(pre_example)
        examples.append(example_html)      
    examples_html = ''.join(examples)  
    return examples_html        
