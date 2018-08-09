from flask import Blueprint, render_template, request, url_for
from xray_app.methods.forms import Xraylib_Request, Request_Error,  Request_Units
from xray_app.methods.utils import validate_int, validate_float, validate_str, validate_int_or_str, code_example, make_tup, check_xraylib_key
import xraylib

methods = Blueprint('methods', __name__)

#eventually move to own package e.g. xray_app.methods.validators, then import
#ditto for the dicts

            
#def validate_NIST(s) etc
#------------------------------------------------------------------------------------------------------------       
def calc_output(function, *values):
    function = getattr(xraylib, function)
    lst = []
    for value in values:
        if validate_int(value) == True and float(value) == int(value):
            lst.append(int(value))
        elif validate_float(value) == True:
            lst.append(float(value))  
        elif check_xraylib_key(str(value)) == True:
            value = getattr(xraylib, value)
            lst.append(value) 
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            lst.append(xraylib.SymbolToAtomicNumber(value))
        else:
            lst.append(value)     
    print(lst)        
    output = float(function(*lst))
    return output
#------------------------------------------------------------------------------------------------------------
nist_dict = {xraylib.GetCompoundDataNISTByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('NIST')}
rad_dict = {xraylib.GetRadioNuclideDataByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('RADIO')}
shell_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('SHELL')}
ck_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('TRANS')}
aug_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('AUGER')}
trans_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('_LINE')}
cs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('CS_') and not k.endswith('CP')} 
dcs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('DCS_')and not k.endswith('CP') or k.startswith('DCSP_') and not k.endswith('CP')}      

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
            examples = request.form.get('examples')
                
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
            
            if select_input == 'AtomicWeight':
                code_examples = code_example(form.examples.choices, select_input, int_z)
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                    output = calc_output(select_input, int_z)                    
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.AtomicWeight_u,
                        code_examples = code_examples
                        )                
                else:
                        return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                                
            elif select_input == 'ElementDensity':
                code_examples = code_example(form.examples.choices, select_input, int_z)
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                    output = calc_output(select_input, int_z)                        
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.ElementDensity_u,
                        code_examples = code_examples
                        )                
                else:
                        return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )

            elif select_input == 'FF_Rayl':
                code_examples = code_example(form.examples.choices, select_input, int_z, float_q)
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0 and validate_float(float_q) == True:
                    output = calc_output(select_input, int_z, float_q)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        code_examples = code_examples
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
                code_examples = code_example(form.examples.choices, select_input, int_z, float_q)
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0 and validate_float(float_q) == True:
                    output = calc_output(select_input, int_z, float_q)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        code_examples = code_examples
                        )                
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
            
            elif select_input == 'LineEnergy':
                if linetype_trans_notation == 'IUPAC':
                    code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_iupac)
                    trans = getattr(xraylib, linetype_trans_iupac)
                    if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                        output = calc_output(select_input, int_z, trans)
                        #output = xraylib.LineEnergy(int(int_z), trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.Energy_u,
                            code_examples = code_examples
                            )                    
                elif linetype_trans_notation == 'Siegbahn':
                    code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_siegbahn)
                    trans = getattr(xraylib, linetype_trans_siegbahn)
                    if validate_int(int_z) == True:
                        output = calc_output(select_input, int_z, trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.Energy_u,
                            code_examples = code_examples
                            )                     
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
                        
            elif select_input == 'RadRate':
                if linetype_trans_notation == 'IUPAC':
                    code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_iupac)
                    trans = getattr(xraylib, linetype_trans_iupac)
                    if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                        output = calc_output(select_input, int_z, trans)                       
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            code_examples = code_examples
                            )                    
                elif linetype_trans_notation == 'Siegbahn':
                    code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_siegbahn)
                    trans = getattr(xraylib, linetype_trans_siegbahn)
                    if validate_int(int_z) == True:
                        output = calc_output(select_input, int_z, trans)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            code_examples = code_examples
                            )                     
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
                        
            elif select_input == 'EdgeEnergy':
                code_examples = code_example(form.examples.choices, select_input, int_z, shell)
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:                    
                    shell = getattr(xraylib, shell)
                    output = calc_output(select_input, int_z, shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.Energy_u,
                        code_examples = code_examples
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                        
            elif select_input == 'FluorYield':
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                    shell = getattr(xraylib, shell)
                    output = calc_output(select_input, int_z, shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        code_examples = code_examples
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                        
            elif select_input == 'AugerYield':
                code_examples = code_example(form.examples.choices, select_input, int_z, shell)
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                    shell = getattr(xraylib, shell)
                    output = calc_output(select_input, int_z, shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        code_examples = code_examples
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )   
            
            elif select_input == 'JumpFactor':
                code_examples = code_example(form.examples.choices, select_input, int_z, shell)
                if validate_int(int_z) == True:
                    shell = getattr(xraylib, shell)
                    output = calc_output(select_input, int_z, shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        code_examples = code_examples
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                        
            elif select_input == 'AtomicLevelWidth':
                code_examples = code_example(form.examples.choices, select_input, int_z, shell)
                if validate_int(int_z) == True:
                    shell = getattr(xraylib, shell)
                    output = calc_output(select_input, int_z, shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        code_examples = code_examples
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        ) 
                             
            elif select_input == 'ElectronConfig':
                code_examples = code_example(form.examples.choices, select_input, int_z, shell)
                if validate_int(int_z) == True:
                    shell = getattr(xraylib, shell)
                    output = calc_output(select_input, int_z, shell)
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.ElectronConfig_u,
                        code_examples = code_examples 
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )
                
            elif select_input == 'CS_Total':
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy)
                print(f'int_z_or_comp: {int_z_or_comp}' + f'energy: {energy}')
                #need to add in CSb
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy) == True:
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Total(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, code_examples = code_examples
                            )
                    except ValueError:
                        output = xraylib.CS_Total_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
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
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy) == True:
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Photo(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, code_examples = code_examples
                            )
                    except ValueError:
                        output = xraylib.CS_Photo_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, code_examples = code_examples
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
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy) == True:
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Rayl(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, code_examples = code_examples
                            )
                    except ValueError:
                        output = xraylib.CS_Rayl_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, code_examples = code_examples
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
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy) == True:
                    #NOTE comp input is case sensitive
                    try:
                        output = xraylib.CS_Compt(int(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, code_examples = code_examples
                            )
                    except ValueError:
                        output = xraylib.CS_Compt_CP(str(int_z_or_comp), float(energy))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, code_examples = code_examples
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
            
            elif select_input == 'CS_FluorLine':
                if validate_int(int_z) == True and validate_float(energy) == True:
                    if linetype_trans_notation == 'IUPAC':
                        print(f'int_z: {int_z}' + ' ' + f'linetype_trans_notation: {linetype_trans_notation}' + ' ' + f'linetype_trans_iupac: {linetype_trans_iupac}')
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.CS_FluorLine(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, code_examples = code_examples
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output  = xraylib.CS_FluorLine(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, code_examples = code_examples
                            )
                    else:
                        return render_template(
                            'index.html', 
                            form = form,
                            error=error
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
                            output = output, code_examples = code_examples
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output  = xraylib.CS_FluorLine_Kissel_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, code_examples = code_examples
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
                            output = output, code_examples = code_examples
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output  = xraylib.CS_FluorLine_Kissel_Radiative_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            )
                    else:
                        return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )
                             
            elif select_input == 'CS_FluorLine_Kissel_Nonradiative_Cascade':
                if validate_int(int_z) == True and validate_float(energy) == True:
                    if linetype_trans_notation == 'IUPAC':
                        print(f'int_z: {int_z}' + ' ' + f'linetype_trans_notation: {linetype_trans_notation}' + ' ' + f'linetype_trans_iupac: {linetype_trans_iupac}')
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.CS_FluorLine_Kissel_Nonradiative_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output  = xraylib.CS_FluorLine_Kissel_Nonradiative_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            )
                    else:
                        return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )   
                            
            elif select_input == 'CS_FluorLine_Kissel_no_Cascade':
                if validate_int(int_z) == True and validate_float(energy) == True:
                    if linetype_trans_notation == 'IUPAC':
                        print(f'int_z: {int_z}' + ' ' + f'linetype_trans_notation: {linetype_trans_notation}' + ' ' + f'linetype_trans_iupac: {linetype_trans_iupac}')
                        trans = getattr(xraylib, linetype_trans_iupac)
                        output = xraylib.CS_FluorLine_Kissel_no_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            ) 
                    elif linetype_trans_notation == 'Siegbahn':
                        trans = getattr(xraylib, linetype_trans_siegbahn)
                        output  = xraylib.CS_FluorLine_Kissel_no_Cascade(int(int_z), trans, float(energy))
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
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
                            output = output, examples = examples
                            )
                elif xraylib.SymbolToAtomicNumber(int_z) != 0:
                    shell = getattr(xraylib, shell)
                    output = xraylib.CS_Photo_Partial(int(xraylib.SymbolToAtomicNumber(int_z)), shell, float(energy))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
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
                            output = output, examples = examples
                            )
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )   
            
            elif select_input == 'DCS_Thoms':
                if validate_float(theta) == True:
                    output = xraylib.DCS_Thoms(float(theta))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            )
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )
                            
            elif select_input == 'DCS_KN':
                if validate_float(energy, theta) == True:
                    output = xraylib.DCS_KN(float(energy), float(theta))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            )
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )
                            
            elif select_input == 'ComptonEnergy':
                if validate_float(energy, theta) == True:
                    output = xraylib.ComptonEnergy(float(energy), float(theta))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            )
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            ) 
            
            elif select_input == 'DCS_Rayl':
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy, theta) == True:
                    try:
                        output = xraylib.DCS_Rayl(int(int_z_or_comp), float(energy), float(theta))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
                            )
                    except ValueError:
                        output = xraylib.DCS_Rayl_CP(str(int_z_or_comp), float(energy), float(theta))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
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
                            
            elif select_input == 'DCS_Compt':
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy, theta) == True:
                    try:
                        output = xraylib.DCS_Compt(int(int_z_or_comp), float(energy), float(theta))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
                            )
                    except ValueError:
                        output = xraylib.DCS_Compt_CP(str(int_z_or_comp), float(energy), float(theta))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
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
            
            elif select_input == 'DCSP_Thoms':
                if validate_float(theta, phi) == True:
                    output = xraylib.DCSP_Thoms(float(theta), float(phi))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            )
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            )
                            
            elif select_input == 'DCSP_KN':
                if validate_float(energy, theta, phi) == True:
                    output = xraylib.DCSP_KN(float(energy), float(theta), float(phi))
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output, examples = examples
                            )
                else:
                   return render_template(
                            'index.html', 
                            form = form,
                            error=error
                            ) 
                                           
            elif select_input == 'DCSP_Rayl':
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy, theta, phi) == True:
                    try:
                        output = xraylib.DCSP_Rayl(int(int_z_or_comp), float(energy), float(theta), float(phi))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
                            )
                    except ValueError:
                        output = xraylib.DCSP_Rayl_CP(str(int_z_or_comp), float(energy), float(theta), float(phi))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
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
            
            elif select_input == 'DCSP_Compt':
                if validate_int_or_str(int_z_or_comp) == True and validate_float(energy, theta, phi) == True:
                    try:
                        output = xraylib.DCSP_Compt(int(int_z_or_comp), float(energy), float(theta), float(phi))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
                            )
                    except ValueError:
                        output = xraylib.DCSP_Compt_CP(str(int_z_or_comp), float(energy), float(theta), float(phi))
                        return render_template(
                            'index.html',
                            form = form, 
                            output = output, examples = examples
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
            #missing cs_energy and total kissel            
            
            elif select_input == 'Refractive_Index':
                if validate_str(str(comp)) == True and validate_float(energy, density) == True:
                    output = xraylib.Refractive_Index(comp, float(energy), float(density))
                    return render_template(
                        'index.html',
                        form = form, 
                        output = output, examples = examples
                        )
                elif validate_str(comp) == False:
                    output = xraylib.Refractive_Index(xraylib.AtomicNumberToSymbol(comp), float(energy), float(density))
                    
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.comp_error
                        )
                else:
                     return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.energy_error
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
                    output = output, examples = examples
                    )
                
            elif select_input == 'GetCompoundDataNISTByName':
                print (f'nistcomp: {nistcomp}')
                output = xraylib.GetCompoundDataNISTByName(str(nistcomp))
                return render_template(
                    'index.html',
                    form = form, 
                    output = output, examples = examples
                    )         
        return render_template('index.html', form=form) 

