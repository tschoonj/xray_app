from flask import Blueprint, render_template, request, url_for
#from xray_app import app - remove me?
from xray_app.methods.forms import Xraylib_Request, Request_Error,  Request_Units
import xraylib

methods = Blueprint('methods', __name__)

#eventually move to own package e.g. xray_app.methods.validators, then import
#ditto for the dicts
def validate_int(s):
        try: 
                int(s)
                return True
        except ValueError:
                return False
        
def validate_float(s):
        try: 
                float(s)
                return True
        except ValueError:
                return False
                
def validate_str(s):
        try:
            str(s)
            return True
        except ValueError:
            return False
            
def validate_int_or_str(s):
    try:
        int(s)
        return True
    except ValueError:
        try:
            str(s)
            return True
        except ValueError:
            return False
            
#def validate_NIST(s) etc
#------------------------------------------------------------------------------------------------------------
def code_example(tple, function):
    languages = [x[0] for x in tple]
    language_labels = [x[1] for x in tple]
    print(languages)
    for label in language_labels:
        support = 'Enable support for xraylib in' + str(label) + 'using: '
    for language in languages:
        pass
        
def calc_output(function, *value):
    function = getattr(xraylib, function)
    output = float(function(*value))
    return output
#------------------------------------------------------------------------------------------------------------
nist_dict = {xraylib.GetCompoundDataNISTByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('NIST')}
rad_dict = {xraylib.GetRadioNuclideDataByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('RADIO')}
shell_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('SHELL')}
ck_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('TRANS')}
aug_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('AUGER')}
trans_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('_LINE')}
cs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('CS_') and not k.endswith('CP')} 
dcs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('DCS_') or k.startswith('DCSP_')}
      
def make_tup(_dict):
    tup = [(k, k) for k, v in _dict.items()]
    return tup

cs_tup = make_tup(cs_dict)
dcs_tup = make_tup(dcs_dict)

nist_tup = make_tup(nist_dict)
rad_name_tup = make_tup(rad_dict)
shell_tup = make_tup(shell_dict)
ck_tup = make_tup(ck_dict) #need to map more useful names - is it poss to do similar thing as rad_nuc (.replace())
aug_tup = make_tup(aug_dict)
trans_tup = [(k, k) for k, v in trans_dict.items()]
trans_I_tup =  trans_tup[0:383]
trans_S_tup = trans_tup[:382:-1]
trans_S_tup = trans_S_tup[::-1]
#------------------------------------------------------------------------------------------------------------
@methods.route("/", methods=['GET', 'POST'])
def index():
        form = Xraylib_Request()
        form.function.choices = form.function.choices + cs_tup + dcs_tup
        
        #for i in form.examples.choices:
            #print(i)
        
        form.linetype.trans_iupac.choices = trans_I_tup
        form.linetype.trans_siegbahn.choices = trans_S_tup
        form.shell.choices =  shell_tup
        form.cktrans.choices = ck_tup
        form.nistcomp.choices = nist_tup
        form.augtrans.choices = aug_tup
        form.rad_nuc_name.choices = rad_name_tup

        #after separating trans_tup - need if statement on radio click so only relevant trans show JQuery 
        #poss could def populate_choices in separate dict package then call here 
           
        if request.method == 'POST':        
            #for key in request.form.keys():
            #print(f'key= {key}')
                
            select_input = request.form.get('function')
            examples = request.form.get('code_example')
                
            linetype_trans_notation = request.form.get('linetype-trans_notation')
            linetype_trans_iupac = request.form.get('linetype-trans_iupac')
            linetype_trans_siegbahn = request.form.get('linetype-trans_siegbahn')
            cktrans = request.form.get('cktrans')
            nistcomp = request.form.get('nistcomp')
            augtrans = request.form.get('augtrans')
            rad_nuc_name = request.form.get('rad_nuc_name')
            shell = request.form.get('shell')
             #print(shell)
             #print(linetype_trans_notation)
                
            int_z = request.form['int_z']
            float_q = request.form['float_q']
            comp = request.form['comp']
            int_z_or_comp = request.form['int_z_or_comp']
            energy = request.form['energy']
            theta = request.form['theta']
            phi = request.form['phi']
            density = request.form['density']
            pz = request.form['pz']
            
            """def z_input(function, int_z):
                print(int_z)
                if validate_int(int_z) == True and 0<int(int_z)<=118:                
                    print(f'int_z: {int_z}')
                    function = getattr(xraylib, function)
                    output = function(int(int_z))
                    print(output) 
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.AtomicWeight_u
                        )
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    function = getattr(xraylib, function)
                    output = function(int(xraylib.SymbolToAtomicNumber(int_z))) 
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.AtomicWeight_u
                            )
                else:
                    return render_template(
                        'index.html',
                        form = form,
                        error = Request_Error.int_z_error
                        )"""

            
            if select_input == 'AtomicWeight':
                if validate_int(int_z) == True and 0<int(int_z)<=118:
                    print(f'int_z: {int_z}')
                    output = calc_output('AtomicWeight', int(int_z))
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.AtomicWeight_u
                        )                
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    output = calc_output('AtomicWeight', int(xraylib.SymbolToAtomicNumber(int_z)))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.AtomicWeight_u
                            )
                else:
                        return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                                
            elif select_input == 'ElementDensity':
                if validate_int(int_z) == True and 0<int(int_z)<=118:
                    print(f'int_z: {int_z}')
                    output = xraylib.ElementDensity(int(int_z))
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.ElementDensity_u
                        )                
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    output = xraylib.ElementDensity(int(xraylib.SymbolToAtomicNumber(int_z)))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.ElementDensity_u
                            )
                else:
                        return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )

            elif select_input == 'FF_Rayl':
                if validate_int(int_z) == True and validate_float(float_q) == True and 0<int(int_z)<=118:
                    print(f'int_z: {int_z}' + f'float_q: {float_q}')
                    output = xraylib.FF_Rayl(int(int_z), float(float_q))
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    rayl_ff=xraylib.FF_Rayl(int(xraylib.SymbolToAtomicNumber(int_z)), float(float_q))       
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                elif validate_float(float_q) == False:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error=Request_Error.float_q_error
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )    
            
            elif select_input == 'SF_Compt':
                if validate_int(int_z) == True and validate_float(float_q) == True and 0<int(int_z)<=118:
                    print(f'int_z: {int_z}' + f'float_q: {float_q}')
                    output = xraylib.SF_Compt(int(int_z), float(float_q))
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    output = xraylib.SF_Compt(int(xraylib.SymbolToAtomicNumber(int_z)), float(float_q))
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
            
            elif select_input == 'LineEnergy':
                if validate_int(int_z) == True:
                    print(f'int_z: {int_z}' + ' ' + f'linetype_trans_notation: {linetype_trans_notation}' + '' + f'linetype_trans_iupac: {linetype_trans_iupac}')
                    if linetype_trans_notation == 'IUPAC':
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.LineEnergy(int(int_z), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output = xraylib.LineEnergy(int(int_z), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            )     
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    if linetype_trans_notation == 'IUPAC':
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.LineEnergy(int(xraylib.SymbolToAtomicNumber(int_z)), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output = xraylib.LineEnergy(int(xraylib.SymbolToAtomicNumber(int_z)), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
                        
            elif select_input == 'RadRate':
                if validate_int(int_z) == True:
                    if linetype_trans_notation == 'IUPAC':
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.RadRate(int(int_z), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output = xraylib.RadRate(int(int_z), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            )         
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    if linetype_trans_notation == 'IUPAC':
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.RadRate(int(xraylib.SymbolToAtomicNumber(int_z)), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output = xraylib.RadRate(int(xraylib.SymbolToAtomicNumber(int_z)), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
                        
            elif select_input == 'EdgeEnergy':
                if validate_int(int_z) == True:
                    print(f'int_z: {int_z}' + ' ' + f'shell: {shell}')
                    shell = getattr(xraylib, shell)
                    output = xraylib.EdgeEnergy(int(int_z), shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                        
            elif select_input == 'FluorYield':
                if validate_int(int_z) == True:
                    print(f'int_z: {int_z}' + ' ' + f'shell: {shell}')
                    shell = getattr(xraylib, shell)
                    output = xraylib.FluorYield(int(int_z), shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                        
            elif select_input == 'AugerYield':
                if validate_int(int_z) == True:
                    print(f'int_z: {int_z}' + ' ' + f'shell: {shell}')
                    shell = getattr(xraylib, shell)
                    output = xraylib.AugerYield(int(int_z), shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )   
            
            elif select_input == 'JumpFactor':
                if validate_int(int_z) == True:
                    print(f'int_z: {int_z}' + ' ' + f'shell: {shell}')
                    shell = getattr(xraylib, shell)
                    output = xraylib.JumpFactor(int(int_z), shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                        
            elif select_input == 'AtomicLevelWidth':
                if validate_int(int_z) == True:
                    print(f'int_z: {int_z}' + ' ' + f'shell: {shell}')
                    shell = getattr(xraylib, shell)
                    output = xraylib.AtomicLevelWidth(int(int_z), shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        ) 
                             
            elif select_input == 'ElectronConfig':
                if validate_int(int_z) == True:
                    print(f'int_z: {int_z}' + ' ' + f'shell: {shell}')
                    shell = getattr(xraylib, shell)
                    output = xraylib.ElectronConfig(int(int_z), shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.ElectronConfig_u 
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                
            elif select_input == 'CS_Total':
                print(f'int_z_or_comp: {int_z_or_comp}' + f'energy: {energy}')
                #need to add in CSb
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy):
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Total(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                    except ValueError:
                        output = xraylib.CS_Total_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                elif validate_int_or_str(int_z_or_comp) == False:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_or_comp_error
                        )
                else:
                     return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.energy_error
                        )
                        
            elif select_input == 'CS_Photo':
                print(f'int_z_or_comp: {int_z_or_comp}' + f'energy: {energy}')
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy):
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Photo(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                    except ValueError:
                        output = xraylib.CS_Photo_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                elif validate_int_or_str(int_z_or_comp) == False:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_or_comp_error
                        )
                else:
                     return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.energy_error
                        )
                              
            elif select_input == 'CS_Rayl':
                print(f'int_z_or_comp: {int_z_or_comp}' + f'energy: {energy}')
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy):
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Rayl(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                    except ValueError:
                        output = xraylib.CS_Rayl_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                elif validate_int_or_str(int_z_or_comp) == False:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_or_comp_error
                        )
                else:
                     return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.energy_error
                        )
            
            elif select_input == 'CS_Compt':
                print(f'int_z_or_comp: {int_z_or_comp}' + f'energy: {energy}')
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy):
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Compt(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                    except ValueError:
                        output = xraylib.CS_Compt_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output
                            )
                elif validate_int_or_str(int_z_or_comp) == False:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_or_comp_error
                        )
                else:
                     return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.energy_error
                        )
                                     
            elif select_input == 'CS_FluorLine_Kissel_Cascade':
                if validate_int(int_z) == True and validate_float(energy) == True:
                    if linetype_trans_notation == 'IUPAC':
                        print(f'int_z: {int_z}' + ' ' + f'linetype_trans_notation: {linetype_trans_notation}' + ' ' + f'linetype_trans_iupac: {linetype_trans_iupac}')
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.CS_FluorLine_Kissel_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output  = xraylib.CS_FluorLine_Kissel_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            )
                    else:
                        return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )
            
            elif select_input == 'CS_FluorLine_Kissel_Radiative_Cascade':
                if validate_int(int_z) == True and validate_float(energy) == True:
                    if linetype_trans_notation == 'IUPAC':
                        print(f'int_z: {int_z}' + ' ' + f'linetype_trans_notation: {linetype_trans_notation}' + ' ' + f'linetype_trans_iupac: {linetype_trans_iupac}')
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.CS_FluorLine_Kissel_Radiative_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output  = xraylib.CS_FluorLine_Kissel_Radiative_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            )
                    else:
                        return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            ) 
                                               
            elif select_input == 'CS_Photo_Partial':                     
                if validate_int(int_z) == True and validate_float(energy) == True:
                    shell = getattr(xraylib, shell)
                    output = xraylib.CS_Photo_Partial(int(int_z), shell, float(energy)) 
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            )
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    shell = getattr(xraylib, shell)
                    output = xraylib.CS_Photo_Partial(int(xraylib.SymbolToAtomicNumber(int_z)), shell, float(energy))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            ) 
                else:  
                     return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )
                            
            elif select_input == 'CS_KN':
                if validate_float(energy) == True:
                    output = xraylib.CS_KN(float(energy))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output
                            )
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )   
            
            elif select_input == '':
                if validate_int(int_z) == True:
                    pass
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )
                              
            elif select_input == 'GetRadioNuclideDataByName':
                print (f'rad_nuc_name: {rad_nuc_name}')
                output = xraylib.GetRadioNuclideDataByName(str(rad_nuc_name))
                return render_template(
                    'index.html',
                    form = form,
                    output = output
                    )
                
            elif select_input == 'GetCompoundDataNISTByName':
                print (f'nistcomp: {nistcomp}')
                output = xraylib.GetCompoundDataNISTByName(str(nistcomp))
                return render_template(
                    'index.html',
                    form = form, 
                    output = output
                    )         
        return render_template('index.html', form=form) 

