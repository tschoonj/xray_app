import xraylib

from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

def validate_float(*s):
    for i in s:
        try: 
            float(i)
            return True
        except ValueError:
            return False

def validate_int(s):
    try:
        if float(s) == int(s):
            return True
        else:
            return False
    except:
        return False
                
def validate_str(*s):
    for i in s:
        try: 
            str(i)
            return True
        except ValueError:
            return False
            
def validate_int_or_str(*s):
    for i in s:
        try:
            int(i)
            return True
        except ValueError:
            try:
                str(i)
                return True
            except ValueError:
                return False
                
#------------------------------------------------------------------------------------------------
def make_tup(_dict):
    tup = [(k, k) for k, v in _dict.items()]
    return tup

def check_xraylib_key(s):
    s = s.upper()
    s = s.replace(" ", "_")
    s = s.replace("-", "_")
       
    for key in xraylib.__dict__:
        #print (key)
        if s in key:
            #print (key)
            print ("found")
            return True
        else:
            if key.endswith('_' + s):
                #print (key) 
                #print("found at end")
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
    lst = []
    """if function == 'Refractive_Index':
        value1 = values[0]
        if validate_int(value1) == True:
            lst.append(xraylib.AtomicNumberToSymbol(int(value1)))
        #else validate_str(value)
        try in for turning values into list then removing
        """
    for value in values:
        print(value)
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
            
    print(lst)
    try:
        output = xrl_function(*lst)
        print(output)
        return output
    except:
        try:
            xrl_function = getattr(xraylib, function + '_CP')
            output = xrl_function(*lst)
            print(output)
            return output
        except:
            output = 'Error'
            print(output)
            return output

def code_example(tple, function, *variables):
    languages = [x[0] for x in tple]
    labels = [x[1] for x in tple]
    examples = []
       
    for label in labels:
        if label == 'C/C++/Objective-C':
            support = '#include <xraylib.h>'
        elif label == 'Fortran 2003/2008':
            support = 'use :: xraylib'
        elif label == 'Perl':
            support = 'use xraylib.pm;'
        elif label == 'IDL':
            support = '@xraylib'
        elif label == 'Python':
            support = 'import xraylib'
        elif label == 'Java':
            support = 'import com.github.tschoonj.xraylib.*;'
        elif label == 'C#/.NET':
            support = 'using Science;'
        elif label == 'Lua':
            support = 'require("xraylib")'
        elif label == 'Ruby':
            support = 'require \'xraylib\''
        elif label == 'PHP':
            support = 'include("xraylib.php");'
        string = 'Enable support for xraylib in ' + str(label) + ' using: <br>' + str(support) + '<br>'
        examples.append(string)
        
    for language in languages:
        #ADD DIVS/ID SO CSS CAN WORK
        lst = []
        lexer = get_lexer_by_name(language)
        print(lexer)
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
        example = highlight(example, lexer, HtmlFormatter())    
        examples.append(example)      
    examples_html = ''.join(examples)  
    return examples_html        
