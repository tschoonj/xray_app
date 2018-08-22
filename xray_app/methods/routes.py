from flask import Blueprint, render_template, request, url_for

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import xraylib

from xray_app.methods.forms import Xraylib_Request, Request_Error,  Request_Units
from xray_app.methods.utils import validate_int, validate_float, validate_str , validate_int_or_str, code_example, make_tup, check_xraylib_key, calc_output, label_dict, all_trans, all_trans_xrf



methods = Blueprint('methods', __name__)

#eventually move to own package e.g. xray_app.methods.validators, then import
#ditto for the dicts
#------------------------------------------------------------------------------------------------------------
nist_dict = {xraylib.GetCompoundDataNISTByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('NIST')}
rad_dict = {xraylib.GetRadioNuclideDataByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('RADIO')}

shell_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('SHELL')}
ck_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('TRANS')}
aug_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('AUGER')}
trans_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('_LINE')}
cs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('CS_') and not k.endswith('CP')} 
dcs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('DCS_')and not k.endswith('CP') or k.startswith('DCSP_') and not k.endswith('CP')}      

  
cs_tup = make_tup(cs_dict, 'cs') #special case
dcs_tup = make_tup(dcs_dict, 'dcs') #special case
nist_tup = make_tup(nist_dict, 'nist')
rad_name_tup = make_tup(rad_dict, 'rad')
shell_tup = make_tup(shell_dict, 'shell')
ck_tup = make_tup(ck_dict, 'ck')  #special case
aug_tup = make_tup(aug_dict, 'aug')

trans_tup = [(k, k.split('_')[0]) for k, v in trans_dict.items()]
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
    form.rad_nuc.choices = rad_name_tup


        #after separating trans_tup - need if statement on radio click so only relevant trans show JQuery 
        #poss could def populate_choices in separate dict package then call here 
           
    if request.method == 'POST':        
            #for key in request.form.keys():
                #print(f'key= {key}')
                
        select_input = request.form.get('function')
        print(select_input)
        examples = request.form.get('examples')
                
        linetype_trans_notation = request.form.get('linetype-trans_notation')
        linetype_trans_iupac = request.form.get('linetype-trans_iupac')
        linetype_trans_siegbahn = request.form.get('linetype-trans_siegbahn')
        cktrans = request.form.get('cktrans')
        nistcomp = request.form.get('nistcomp')
        augtrans = request.form.get('augtrans')
        rad_nuc = request.form.get('rad_nuc')
        shell = request.form.get('shell')
                
        int_z = request.form['int_z']
        float_q = request.form['float_q']
        comp = request.form['comp']
        int_z_or_comp = request.form['int_z_or_comp']
        energy = request.form['energy']
        theta = request.form['theta']
        phi = request.form['phi']
        density = request.form['density']
        pz = request.form['pz']
          
        if select_input == 'AtomicWeight' or select_input == 'ElementDensity':
            if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                examples = code_example(form.examples.choices, select_input, int_z)               
                output = calc_output(select_input, int_z)                    
                return render_template(
                    'index.html', 
                    form = form,
                    output = output,
                    units = getattr(Request_Units, select_input + '_u'),
                    code_examples = examples
                    )                
            else:
                return render_template(
                    'index.html', 
                    form = form,  
                    error = Request_Error.error
                    )
                       
        elif select_input == 'FF_Rayl' or select_input == 'SF_Compt':
            if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                code_examples = code_example(form.examples.choices, select_input, int_z, float_q)
                output = calc_output(select_input, int_z, float_q)
                return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        code_examples = code_examples)                        
            else:
                return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )    

        elif select_input == 'LineEnergy' or select_input == 'RadRate':
            if linetype_trans_notation == 'IUPAC':
                #trans = getattr(xraylib, linetype_trans_iupac)
                if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                    code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_iupac)
                    output = calc_output(select_input, int_z, linetype_trans_iupac)
                        #output = xraylib.LineEnergy(int(int_z), trans)
                    if select_input == 'LineEnergy':
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
                                output = output,
                                code_examples = code_examples
                                )                    
            elif linetype_trans_notation == 'Siegbahn':
                if validate_int_or_float(int_z) == True:
                    code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_siegbahn)
                    output = calc_output(select_input, int_z, linetype_trans_siegbahn)
                    if select_input == 'LineEnergy':
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
                            output = output,
                            code_examples = code_examples
                            )                      
            elif linetype_trans_notation == 'All':
                output = all_trans(form.linetype.trans_iupac.choices, select_input, int_z)
                if select_input == 'LineEnergy':
                    return render_template(
                                'index.html', 
                                form = form,
                                output = output,
                                units = Request_Units.Energy_u
                                )
                else:
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
        elif select_input == 'EdgeEnergy' or select_input == 'JumpFactor' or select_input == 'FluorYield' or select_input == 'AugerYield' or select_input == 'AtomicLevelWidth' or select_input == 'ElectronConfig':
            if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:                    
                code_examples = code_example(form.examples.choices, select_input, int_z, shell)
                output = calc_output(select_input, int_z, shell)
                if select_input == 'EdgeEnergy' or select_input == 'AtomicLevelWidth':
                    return render_template(
                        'index.html', 
                        form = form,
                        output = output,
                        units = Request_Units.Energy_u,
                        code_examples = code_examples
                        )
                elif select_input == 'ElectronConfig':
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
                        output = output,
                        code_examples = code_examples
                        )
            else:
                return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.int_z_error
                        )

        elif select_input == 'CS_Photo_Partial':
            if validate_int(int_z) or xraylib.SymbolToAtomicNumber(int_z) != 0 and validate_float(energy):
                output = calc_output(select_input, int_z, shell, energy)
                code_examples = code_example(form.examples.choices, select_input, int_z, shell, energy)  
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.CS_u, 
                            code_examples = code_examples
                            )
            else:
                return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
         
        elif select_input == 'CS_KN':
            if validate_float(energy) == True:
                output = calc_output(select_input, energy)
                code_examples = code_example(form.examples.choices, select_input, energy)
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.CS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error=Request_Error.error
                            )
                            
        elif select_input.startswith('CS_FluorLine'):
            if validate_float(energy) == True:
                if linetype_trans_notation == 'IUPAC':
                    if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                        code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_iupac, energy)
                        output = calc_output(select_input, int_z, linetype_trans_iupac, energy)
                        return render_template(
                                'index.html', 
                                form = form,
                                output = output,
                                units = Request_Units.CS_u, 
                                code_examples = code_examples
                                )
                elif linetype_trans_notation == 'Siegbahn':
                    if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                        code_examples = code_example(form.examples.choices, select_input, int_z, linetype_trans_siegbahn, energy)
                        output = calc_output(select_input, int_z, linetype_trans_siegbahn, energy)
                        return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.CS_u, 
                            code_examples = code_examples
                            )
                elif linetype_trans_notation == 'All':
                    output = all_trans_xrf(form.linetype.trans_iupac.choices, select_input, int_z, energy)
                    return render_template(
                                'index.html', 
                                form = form,
                                output = output,
                                units = Request_Units.CS_u
                                )            
            else:
                return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )                             
        elif select_input.startswith('CS_'):
                #need to add in CSb
            if validate_int_or_str(int_z_or_comp) == True and validate_float(energy) == True:
                    #NOTE comp input is case sensitive
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy)
                output = calc_output(select_input, int_z_or_comp, energy)
                return render_template(
                            'index.html',
                            form = form, 
                            output = output,
                            units = Request_Units.CS_u, 
                            code_examples = code_examples
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
                          
        elif select_input == 'DCS_Thoms':
            if validate_float(theta) == True:
                output = calc_output(select_input, theta)
                code_examples = code_example(form.examples.choices, select_input, theta)
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )
                                     
        elif select_input == 'DCS_KN' or select_input == 'ComptonEnergy':
            if validate_float(energy, theta):
                output = calc_output(select_input, energy, theta)
                code_examples = code_example(form.examples.choices, select_input, energy, theta)
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )     
        
        elif select_input.startswith('DCS_'):
            if validate_float(energy, theta) and validate_int_or_str(int_z_or_comp):
                output = calc_output(select_input, int_z_or_comp, energy, theta)
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, theta)
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )
        
        elif select_input == 'DCSP_KN':
            if validate_float(energy, theta, phi) == True:
                output = calc_output(select_input, energy, theta, phi)
                code_examples = code_example(form.examples.choices, select_input, energy, theta, phi)
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )
                                
        elif select_input == 'DCSP_Thoms':
            if validate_float(theta, phi) == True:
                output = calc_output(select_input, theta, phi)
                code_examples = code_example(form.examples.choices, select_input, theta, phi)
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )
                            
        elif select_input.startswith('DCSP_'):
            if validate_float(energy, theta, phi) == True and validate_int_or_str(int_z_or_comp) == True:
                output = calc_output(select_input, int_z_or_comp, energy, theta, phi)
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, theta, phi)
                return render_template(
                            'index.html', 
                            form = form,
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )                    
        #missing cs_energy and total kissel
        elif select_input.startswith('Fi'):
            if validate_int(int_z) == True or validate_float(energy) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                output = calc_output(select_input, int_z, energy)
                code_examples = code_example(form.examples.choices, select_input, int_z, energy)
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
        
        elif select_input == 'CosKronTransProb':
            if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                output = calc_output(select_input, int_z, cktrans)
                code_examples = code_example(form.examples.choices, select_input, int_z, cktrans)
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
        
        elif select_input == 'ComptonProfile':
            if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                output = calc_output(select_input, int_z, pz)
                code_examples = code_example(form.examples.choices, select_input, int_z, pz)
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
        
        elif select_input == 'ComptonProfile_Partial':
            if validate_int(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                output = calc_output(select_input, int_z, shell, pz)
                code_examples = code_example(form.examples.choices, select_input, int_z, shell, pz)
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
                            
        elif select_input == 'MomentTransf':
            if validate_float(energy, theta) == True:
                output = calc_output(select_input, energy, theta)
                code_examples = code_example(form.examples.choices, select_input, energy, theta)
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
                            
        
        elif select_input == 'Refractive_Index':
            if validate_int_or_str(int_z_or_comp) == True and validate_float(energy, density) == True:
                #calc_output & examples doesn't work bc of the num to symbol thing
                try:
                    output = xraylib.Refractive_Index(xraylib.AtomicNumberToSymbol(int(int_z_or_comp)), float(energy), float(density))
                    code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, density)
                except:
                    output = xraylib.Refractive_Index(int_z_or_comp, float(energy), float(density))
                    code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, density)
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
                        error = Request_Error.energy_error
                        )
        
        elif select_input == 'CompoundParser':
            if validate_str(comp) == True:
                try:
                    output = xraylib.CompoundParser(str(comp))
                    code_examples = code_example(form.examples.choices, select_input, comp)
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output,  
                            code_examples = code_examples
                            )
                except:
                    return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )  
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )                    
                                                                                        
        elif select_input == 'GetRadioNuclideDataList':
            output = xraylib.GetRadioNuclideDataList()
            output.insert(0, '<b> Radionuclides: </b>')
            output = '<br/>'.join(output) 
            code_examples = code_example(form.examples.choices, select_input)
            return render_template(
                    'index.html',  
                    form = form,
                    output = output, 
                    code_examples = code_examples
                    )
        
        elif select_input == 'GetRadioNuclideDataByIndex':
            output = calc_output(select_input, rad_nuc)
            code_examples = code_example(form.examples.choices, 'GetRadioNuclideDataByName', rad_nuc)
            #output = xraylib.GetRadioNuclideDataByName(str(rad_nuc_name))
            return render_template(
                    'index.html',  
                    form = form,
                    output = output, 
                    code_examples = code_examples
                    )
        
        elif select_input == 'GetCompoundDataNISTList':
            output = xraylib.GetCompoundDataNISTList()
            output.insert(0, '<b> NIST Compounds: </b>')
            output = '<br/>'.join(output) 
            code_examples = code_example(form.examples.choices, select_input)
            return render_template(
                    'index.html',  
                    form = form,
                    output = output, 
                    code_examples = code_examples
                    )
                    
        elif select_input == 'GetCompoundDataNISTByIndex':
            output = calc_output(select_input, nistcomp)
            code_examples = code_example(form.examples.choices, 'GetCompoundDataNISTByName', nistcomp)
            return render_template(
                    'index.html',
                    form = form, 
                    output = output,
                    code_examples = code_examples
                    )               
        
        """elif select_input == '':
            if validate_int_or_float(int_z) == True or xraylib.SymbolToAtomicNumber(int_z) != 0:
                output = calc_output(select_input)
                code_examples = code_example(form.examples.choices, select_input)
                pass
            else:
                return render_template(
                            'index.html', 
                            form = form,
                            error = Request_Error.error
                            )"""

    return render_template('index.html', form=form) 
                        
                
