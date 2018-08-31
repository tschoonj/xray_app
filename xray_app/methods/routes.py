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
#generates dicts and tuples needed to populate wtforms choices
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

#slicing transition tuples to split into IUPAC and Siegbahn
trans_tup = [(k, k.split('_')[0]) for k, v in trans_dict.items()]
trans_I_tup =  trans_tup[0:383]
trans_S_tup = trans_tup[:382:-1]
trans_S_tup = trans_S_tup[::-1]                     
#------------------------------------------------------------------------------------------------------------
@methods.route("/", methods=['GET', 'POST'])
def index():
    form = Xraylib_Request()
    
    #populating select fields
    form.function.choices = form.function.choices + cs_tup + dcs_tup    
    form.transition.iupac.choices = trans_I_tup
    form.transition.siegbahn.choices = trans_S_tup
    form.shell.choices =  shell_tup
    form.cktrans.choices = ck_tup
    form.nistcomp.choices = nist_tup
    form.augtrans.choices = aug_tup
    form.rad_nuc.choices = rad_name_tup
           
    if request.method == 'POST':
        #for key in request.form.keys():
            #print(f'key= {key}')
                
        #gets user input for fields
        select_input = request.form.get('function')
        examples = request.form.get('examples')
                
        transition_notation = request.form.get('transition-notation')
        transition_iupac = request.form.get('transition-iupac')
        transition_siegbahn = request.form.get('transition-siegbahn')
        
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
            if validate_int(int_z):
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
            # FF_Rayl accepts float_q = 0, SF_Compt doesn't & no error displayed
            if validate_int(int_z) and validate_float(float_q):
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
            if transition_notation == 'IUPAC':
                if validate_int(int_z):
                    code_examples = code_example(form.examples.choices, select_input, int_z, transition_iupac)
                    output = calc_output(select_input, int_z, transition_iupac)
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
                else:
                    return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )                                        
            elif transition_notation == 'Siegbahn':
                if validate_int(int_z):
                    code_examples = code_example(form.examples.choices, select_input, int_z, transition_siegbahn)
                    output = calc_output(select_input, int_z, transition_siegbahn)
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
                
                return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )                     
            elif transition_notation == 'All':
                if validate_int(int_z):
                    output = all_trans(form.transition.iupac.choices, select_input, int_z)
                    if select_input == 'LineEnergy':
                        #needs units
                        #output = dict(out, Line = 'Energies')
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
            else:
                return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
                        
        elif select_input == 'EdgeEnergy' or select_input == 'JumpFactor' or select_input == 'FluorYield' or select_input == 'AugerYield' or select_input == 'AtomicLevelWidth' or select_input == 'ElectronConfig':
            if validate_int(int_z):                    
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
                        error = Request_Error.error
                        )

        elif select_input == 'CS_Photo_Partial':
            if validate_int(int_z) and validate_float(energy):
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
            if validate_float(energy) and energy != '0':
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
            if validate_float(energy):
                if transition_notation == 'IUPAC':
                    if validate_int(int_z):
                        code_examples = code_example(form.examples.choices, select_input, int_z, transition_iupac, energy)
                        output = calc_output(select_input, int_z, transition_iupac, energy)
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
                elif transition_notation == 'Siegbahn':
                    if validate_int(int_z):
                        code_examples = code_example(form.examples.choices, select_input, int_z, transition_siegbahn, energy)
                        output = calc_output(select_input, int_z, transition_siegbahn, energy)
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
                elif transition_notation == 'All':
                    if validate_int(int_z):
                        output = all_trans_xrf(form.transition.iupac.choices, select_input, int_z, energy)
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
            else:
                return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
                                                     
        elif select_input.startswith('CS_'):
            if validate_int_or_str(int_z_or_comp) and validate_float(energy):
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy)
                output = calc_output(select_input, int_z_or_comp, energy)
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
                          
        elif select_input == 'DCS_Thoms':
            if validate_float(theta):
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
            if validate_float(energy, theta, phi):
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
            if validate_float(energy, theta, phi) and validate_int_or_str(int_z_or_comp):
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
                                                
        elif select_input.startswith('Fi'):
            if validate_int(int_z) or validate_float(energy):
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
            if validate_int(int_z):
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
            if validate_int(int_z):
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
            if validate_int(int_z):
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
            #special case: Refractive_Index input needs to be const char compound
            if validate_int_or_str(int_z_or_comp) and validate_float(energy, density):
                try:
                    output = xraylib.Refractive_Index(xraylib.AtomicNumberToSymbol(int(int_z_or_comp)), float(energy), float(density))
                    code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, density)
                    return render_template(
                        'index.html',
                        form = form, 
                        output = output, 
                        code_examples = code_examples
                        )
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
                        error = Request_Error.error
                        )                
            else:
                     return render_template(
                        'index.html', 
                        form = form,  
                        error = Request_Error.error
                        )
        
        elif select_input == 'CompoundParser':
            #special case: CompoundParser input needs to be const char compound
            #system error doesn't allow for proper validation
            if validate_str(comp) == True:
                try:
                    out = xraylib.CompoundParser(str(comp))
                    
                    #formatting output
                    w_fracts = out['massFractions']
                    w_pers = [str(round(i*100, 2)) + ' %' for i in w_fracts]
                    z = out['Elements']
                    sym = [ '<sub>' + str(i) + '</sub>' + str(xraylib.AtomicNumberToSymbol(i)) for i in z]
                    mmass = str(out['molarMass']) + ' g mol<sup>-1</sup>'
                    
                    output = {'Elements': sym, 'Weight Fraction': w_pers,'Number of Atoms': out['nAtoms'], ' Molar Mass': mmass}
                    code_examples = code_example(form.examples.choices, select_input, comp)
                    return render_template(
                            'index.html', 
                            form = form,
                            output = output,  
                            code_examples = code_examples, 
                            units = Request_Units.per_u
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
            out = calc_output(select_input, rad_nuc)
           
            #formatting output
            line_nos = out['XrayLines']           
            x_energy = [xraylib.LineEnergy(out['Z_xray'], i) for i in line_nos]
            
            output = {'X-ray Energies': x_energy, 'Disintegrations s<sup>-1</sup>': out['XrayIntensities'], 'Gamma-ray Energy': out['GammaEnergies'], 'Disintegrations s<sup>-1</sup> ': out['GammaIntensities']}
            code_examples = code_example(form.examples.choices, 'GetRadioNuclideDataByName', rad_nuc)
            
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
            out = calc_output(select_input, nistcomp)
            
            #formatting output
            w_fracts = out['massFractions']
            w_pers = [str(round(i*100, 2)) + ' %' for i in w_fracts]
            z = out['Elements']
            sym = [ '<sub>' + str(i) + '</sub>' + str(xraylib.AtomicNumberToSymbol(i)) for i in z]
            density = str(out['density']) + ' g cm<sup>-3</sup>'
                    
            output = {'Elements': sym, 'Weight Fraction': w_pers, ' Density': density}
            
            code_examples = code_example(form.examples.choices, 'GetCompoundDataNISTByName', nistcomp)
            return render_template(
                    'index.html',
                    form = form, 
                    output = output,
                    code_examples = code_examples
                    )               

    return render_template('index.html', form=form) 
                        
                
