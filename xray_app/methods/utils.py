import xraylib

from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

def validate_float(*s):
    for i in s:
        try: 
            float(i)
        except ValueError:
            return False
    return True

def validate_int(*s):
    for i in s:
        try:
            if float(i) == int(i):
                return True
            else:
                return False
        except:
            return False
                
def validate_str(*s):
    for i in s:
        try: 
            str(i)
        except ValueError:
            return False
    return True
            
def validate_int_or_str(*s):
    for i in s:
        try:
            int(i)
        except ValueError:
            try:
                str(i)
            except ValueError:
                return False
    return True
#------------------------------------------------------------------------------------------------
def all_trans(tple, *inputs):
    transs = [x[0] for x in tple]
    output = {}    
    for trans in transs:
        out = calc_output(*inputs, trans)
        if out != 0:
            output[trans] = out       
    return output                   
#------------------------------------------------------------------------------------------------
def all_trans_xrf(tple, function, int_z, energy):
    transs = [x[0] for x in tple]
    output = {}
    for trans in transs:
        out = calc_output(function, int_z, trans, energy)
        if out != 0:
            output[trans] = out
    return output
#------------------------------------------------------------------------------------------------
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
        #need to mathc each substr to dict key then 'translate' it        
        

label_dict = {'CS':'Cross Section:', 'DCS':'Differential Unpolarized Cross Section:', 'DCSP':'Differential Polarized Cross Section:', 'KN':'Klein-Nishina', 'Photo':'Photoionization', 'Rayl':'Rayleigh', 'Compt':'Compton', 'FluorLine':' XRF', 'Partial':'(Partial)', 'Thoms':'Thomson', 'TRANS':''}

def check_xraylib_key(s):
    s = s.upper()
    s = s.replace(" ", "_")
    s = s.replace("-", "_")
       
    for key in xraylib.__dict__:
        #print (key)
        if s in key:
            #print (key)
            return True
        else:
            if key.endswith('_' + s):
                #print (key) 
                return True
    return False

def get_key(s):
    s = s.upper()
    s = s.replace(" ", "_")
    s = s.replace("-", "_")
    for key in xraylib.__dict__:
        if s in key:
            return key
        else:
            if key.endswith('_' + s):
                return key 

def calc_output(function, *values):
    xrl_function = getattr(xraylib, function)
    #print(values)

    lst = []
    for value in values:        
        if validate_int(value) == True:
            lst.append(int(value))
        elif validate_float(value) == True:
            lst.append(float(value))   
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            lst.append(xraylib.SymbolToAtomicNumber(value))
        elif check_xraylib_key(value) == True:
            value = get_key(value)
            value = getattr(xraylib, value)
            lst.append(value)
        else:
            lst.append(value)   #needed for _CP entry         
    #print(lst)
    try:
        if validate_int(lst[0]) == True:
            output = xrl_function(*lst)
            #print(output)
            return output
        else: 
            print(function + '_CP')
            print(lst)
            xrl_function = getattr(xraylib, function + '_CP')
            print(xrl_function)
            output = xrl_function(*lst)
            #print(output)
            return output
    except:
        output = 'Error'
        #print(output)

def code_example(tple, function, *variables):
    languages = [x[0] for x in tple]
    labels = [x[1] for x in tple]
    examples = []
       
    for label in labels:
        if label == 'C/C++/Objective-C':
            support = '#include &ltxraylib.h&gt'
            _class = 'cpp-objdump'
        elif label == 'Fortran 2003/2008':
            support = 'use :: xraylib'
            _class = 'fortran'
        elif label == 'Perl':
            support = 'use xraylib.pm;'
            _class = 'perl'
        elif label == 'IDL':
            support = '@xraylib'
            _class = 'idl'
        elif label == 'Python':
            support = 'import xraylib'
            _class = 'python'        
        elif label == 'Java':
            support = 'import com.github.tschoonj.xraylib.*;'
            _class = 'java'
        elif label == 'C#/.NET':
            support = 'using Science;'
            _class = 'antlr-csharp'
        elif label == 'Lua':
            support = 'require("xraylib")'
            _class = 'lua'
        elif label == 'Ruby':
            support = 'require \'xraylib\''
            _class = 'ruby'
        elif label == 'PHP':
            support = 'include("xraylib.php");'
            _class = 'php'
        string = '<div class="'+ str(_class) + ' code-examples"> Enable support for xraylib in ' + str(label) + ' using: <b>' + str(support) + '</b></div>\n'
        examples.append(string)
        
    for language in languages:
        #ADD DIVS/ID SO CSS CAN WORK
        lst = []
        lexer = get_lexer_by_name(language)
        if language == 'cpp-objdump':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append(variable)
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = str(function) + '(' + _input + ')'
        
        elif language == 'fortran':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('symboltoatomicnumber(\'' + variable + '\')')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('$xraylib::' + variable.lower())
                elif function == 'GetRadioNuclideDataByName':
                    lst.append("'55Fe'")
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append("'Acetone'")
            _input = ', '.join(lst)
            example = str(function).lower() + '(' + _input + ')'
        
        elif language == 'perl':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib::SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('$xraylib::' + variable)
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = 'xraylib::' + str(function) + '(' + _input + ')'
        
        elif language == 'idl':
            lst = []
            for variable in variables:
                if validate_float(variable) == True or check_xraylib_key(str(variable)) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SYMBOLTOATOMICNUMBER(\'' + variable + '\')')
                elif function == 'GetRadioNuclideDataByName':
                    lst.append("'55Fe'")
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append("'Acetone'")
            _input = ', '.join(lst)
            example = str(function).upper() + '(' + _input + ')'
        
        elif language == 'python':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('xraylib.' + variable)
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = 'xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'java':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('Xraylib.' + variable)
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'antlr-csharp':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('Xraylib.' + variable)
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'lua':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('xraylib.' + variable)
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = 'xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'ruby':
            for variable in variables:
                if validate_float(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('Xraylib::' + variable)
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'        
        elif language == 'php': 
            for variable in variables:
                if validate_float(variable) == True or check_xraylib_key(str(variable)) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SymbolToAtomicNumber("' + variable + '")')
                elif function == 'GetRadioNuclideDataByName':
                    lst.append('"55Fe"')
                elif function ==  'GetCompoundDataNISTByName':
                    lst.append('"Acetone"')
            _input = ', '.join(lst)
            example = str(function) + '(' + _input + ')'
        example = highlight(example, lexer, HtmlFormatter(cssclass = str(language) + ' code-examples'))
        #print(HtmlFormatter().get_style_defs('.' + str(language))) #prints css
        examples.append(example)      
    examples_html = ''.join(examples)  
    return examples_html        
