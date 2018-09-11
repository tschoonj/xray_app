from flask import Blueprint, render_template, request, url_for

import xraylib

from xray_app.methods.forms import Xraylib_Request, Request_Error,  Request_Units
from xray_app.methods.utils import validate_int, validate_float, validate_str, code_example, make_tup, check_xraylib_key, calc_output, label_dict, all_trans, all_trans_xrf

methods = Blueprint('methods', __name__)
#------------------------------------------------------------------------------------------------------------
# Generates dicts and tuples to populate wtforms choices
nist_dict = {xraylib.GetCompoundDataNISTByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('NIST')}
rad_dict = {xraylib.GetRadioNuclideDataByIndex(int(v))['name']: v for k, v in xraylib.__dict__.items() if k.startswith('RADIO')}
shell_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('SHELL')}

trans_dict = {k: v for k, v in xraylib.__dict__.items() if k.endswith('_LINE')}
cs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('CS_') and not k.endswith('CP')} 
dcs_dict = {k: v for k, v in xraylib.__dict__.items() if k.startswith('DCS_')and not k.endswith('CP') or k.startswith('DCSP_') and not k.endswith('CP')}      
  
cs_tup = make_tup(cs_dict, 'cs')
dcs_tup = make_tup(dcs_dict, 'dcs')
nist_tup = make_tup(nist_dict, 'nist')
rad_name_tup = make_tup(rad_dict, 'rad')
shell_tup = make_tup(shell_dict, 'shell')

# Slices transition tuples into IUPAC and Siegbahn
trans_tup = [(k, k.split('_')[0]) for k, v in trans_dict.items()]
trans_I_tup =  trans_tup[0:383]
trans_S_tup = trans_tup[:382:-1]
trans_S_tup = trans_S_tup[::-1]                     
#------------------------------------------------------------------------------------------------------------
@methods.route("/", methods=['GET', 'POST'])
def index():
    form = Xraylib_Request()
    version = xraylib.__version__
    
    form.function.choices = form.function.choices + cs_tup + dcs_tup
    form.transition.siegbahn.choices = trans_S_tup
    form.shell.choices =  shell_tup
    form.nistcomp.choices = nist_tup
    form.rad_nuc.choices = rad_name_tup
    
    if request.method == 'POST':
        # Get user input
        select_input = request.form.get('function')
        examples = request.form.get('examples')
                
        notation = request.form.get('transition-notation')
        siegbahn = request.form.get('transition-siegbahn')
        iupac1 = request.form.get('transition-iupac1')
        iupac2 = request.form.get('transition-iupac2')        
        
        ex_shell = request.form.get('augtrans-ex_shell')
        trans_shell = request.form.get('augtrans-trans_shell')
        aug_shell = request.form.get('augtrans-aug_shell')
        
        cktrans = request.form.get('cktrans')
        nistcomp = request.form.get('nistcomp')
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
        
        # Turns User Input => valid args for calc_output
        trans = iupac1 + iupac2 + '_LINE'
        augtrans = ex_shell + '_' + trans_shell + aug_shell + '_AUGER'
                       
        if select_input == 'AtomicWeight' or select_input == 'ElementDensity':
            if validate_int(int_z) or validate_str(int_z):
                examples = code_example(form.examples.choices, select_input, int_z)               
                output = calc_output(select_input, int_z)                  
                return render_template(
                    'index.html', 
                    form = form,
                    version = version,
                    output = output,
                    units = getattr(Request_Units, select_input + '_u'),
                    code_examples = examples
                    )                
            else:
                return render_template(
                    'index.html', 
                    form = form, 
                    version = version,   
                    error = Request_Error.error
                    )
                       
        elif select_input == 'FF_Rayl' or select_input == 'SF_Compt':
            if validate_int(int_z) or validate_str(int_z) and validate_float(float_q):
                code_examples = code_example(form.examples.choices, select_input, int_z, float_q)
                output = calc_output(select_input, int_z, float_q)
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version, 
                        output = output,
                        code_examples = code_examples)                        
            else:
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )            

        elif select_input == 'AugerRate':
            if validate_int(int_z) or validate_str(int_z):
                code_examples = code_example(form.examples.choices, select_input, int_z, augtrans)
                output = calc_output(select_input, int_z, augtrans)
                return render_template(
                                'index.html', 
                                form = form, 
                                version = version, 
                                output = output,
                                code_examples = code_examples
                                )
            else:
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )
                
        elif select_input == 'LineEnergy' or select_input == 'RadRate':
            if notation == 'IUPAC':
                if validate_int(int_z) or validate_str(int_z):                    
                    code_examples = code_example(form.examples.choices, select_input, int_z, trans)
                    output = calc_output(select_input, int_z, trans)
                    
                    if select_input == 'LineEnergy':
                        return render_template(
                                'index.html', 
                                form = form, 
                                version = version, 
                                output = output,
                                units = Request_Units.Energy_u,
                                code_examples = code_examples
                                )
                    else:
                        return render_template(
                                'index.html', 
                                form = form, 
                                version = version, 
                                output = output,
                                code_examples = code_examples
                                )
                else:
                    return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )                                        
                  
            elif notation == 'Siegbahn':
                if validate_int(int_z) or validate_str(int_z):
                    code_examples = code_example(form.examples.choices, select_input, int_z, siegbahn)
                    output = calc_output(select_input, int_z, siegbahn)
                    print(output)
                    
                    if select_input == 'LineEnergy':
                        return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.Energy_u,
                            code_examples = code_examples
                            )
                    else:
                        return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            code_examples = code_examples
                            )
                
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )                     
              
            elif notation == 'All':
                if validate_int(int_z) or validate_str(int_z):
                    output = all_trans(trans_I_tup, select_input, int_z)

                    if select_input == 'LineEnergy':
                        #needs units
                        #output = dict(out, Line = 'Energies')
                        return render_template(
                                'index.html', 
                                form = form, 
                                version = version, 
                                output = output,
                                units = Request_Units.Energy_u
                                )
                    else:
                        return render_template(
                                'index.html', 
                                form = form, 
                                version = version, 
                                output = output
                                )
                else:
                    return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )
            else:
                return render_template(
                        'index.html', 
                        error = Request_Error.error
                        )
                        
        elif (select_input == 'EdgeEnergy' or select_input == 'JumpFactor' 
        or select_input == 'FluorYield' or select_input == 'AugerYield' 
        or select_input == 'AtomicLevelWidth' or select_input == 'ElectronConfig'):
            if validate_int(int_z) or validate_str(int_z):                   
                code_examples = code_example(form.examples.choices, select_input, int_z, shell)
                output = calc_output(select_input, int_z, shell)
                if select_input == 'EdgeEnergy' or select_input == 'AtomicLevelWidth':
                    return render_template(
                        'index.html', 
                        form = form, 
                        version = version, 
                        output = output,
                        units = Request_Units.Energy_u,
                        code_examples = code_examples
                        )
                elif select_input == 'ElectronConfig':
                    return render_template(
                        'index.html', 
                        form = form, 
                        version = version, 
                        output = output,
                        units = Request_Units.ElectronConfig_u,
                        code_examples = code_examples
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form, 
                        version = version, 
                        output = output,
                        code_examples = code_examples
                        )
            else:
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )

        elif select_input == 'CS_Photo_Partial':
            if validate_int(int_z) or validate_str(int_z) and validate_float(energy):
                output = calc_output(select_input, int_z, shell, energy)
                code_examples = code_example(form.examples.choices, select_input, int_z, shell, energy)  
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.CS_u, 
                            code_examples = code_examples
                            )
            else:
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )
         
        elif select_input == 'CS_KN':
            if validate_float(energy) and energy != '0':
                output = calc_output(select_input, energy)
                code_examples = code_example(form.examples.choices, select_input, energy)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.CS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            error=Request_Error.error
                            )
                            
        elif select_input.startswith('CS_FluorLine'):
            if validate_float(energy):
                if notation == 'IUPAC':
                    if validate_int(int_z) or validate_str(int_z):
                        code_examples = code_example(form.examples.choices, select_input, int_z, trans, energy)
                        output = calc_output(select_input, int_z, trans, energy)
                        return render_template(
                                'index.html', 
                                form = form, 
                                version = version, 
                                output = output,
                                units = Request_Units.CS_u, 
                                code_examples = code_examples
                                )
                    else:
                        return render_template(
                        'index.html', 
                        form = form,
                        version = version,   
                        error = Request_Error.error
                        )            
                elif notation == 'Siegbahn':
                    if validate_int(int_z) or validate_str(int_z):
                        code_examples = code_example(form.examples.choices, select_input, int_z, siegbahn, energy)
                        output = calc_output(select_input, int_z, siegbahn, energy)
                        return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.CS_u, 
                            code_examples = code_examples
                            )
                    else:
                        return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )        
                elif notation == 'All':
                    if validate_int(int_z) or validate_str(int_z):
                        output = all_trans_xrf(form.transition.iupac.choices, select_input, int_z, energy)
                        return render_template(
                                'index.html', 
                                form = form, 
                                version = version, 
                                output = output,
                                units = Request_Units.CS_u
                                )
                    else:
                        return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )                       
            else:
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )
                                                     
        elif select_input.startswith('CS_'):
            if validate_float(energy) and validate_int(int_z_or_comp) or validate_str(int_z_or_comp):
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy)
                output = calc_output(select_input, int_z_or_comp, energy)
                return render_template(
                            'index.html',
                            form = form, 
                            version = version,  
                            output = output,
                            units = Request_Units.CS_u, 
                            code_examples = code_examples
                            )
            else:
                return render_template(
                        'index.html', 
                        form = form, 
                        version = version,   
                        error = Request_Error.error
                        )
                          
        elif select_input == 'DCS_Thoms':
            if validate_float(theta):
                output = calc_output(select_input, theta)
                code_examples = code_example(form.examples.choices, select_input, theta)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            error = Request_Error.error
                            )
                                     
        elif select_input == 'DCS_KN' or select_input == 'ComptonEnergy':
            if validate_float(energy, theta):
                output = calc_output(select_input, energy, theta)
                code_examples = code_example(form.examples.choices, select_input, energy, theta)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            error = Request_Error.error
                            )     
        
        elif select_input.startswith('DCS_'):
            if validate_float(energy, theta) and validate_int(int_z_or_comp) or validate_str(int_z_or_comp):
                output = calc_output(select_input, int_z_or_comp, energy, theta)
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, theta)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            error = Request_Error.error
                            )
        
        elif select_input == 'DCSP_KN':
            if validate_float(energy, theta, phi):
                output = calc_output(select_input, energy, theta, phi)
                code_examples = code_example(form.examples.choices, select_input, energy, theta, phi)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            error = Request_Error.error
                            )
                                
        elif select_input == 'DCSP_Thoms':
            if validate_float(theta, phi):
                output = calc_output(select_input, theta, phi)
                code_examples = code_example(form.examples.choices, select_input, theta, phi)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            error = Request_Error.error
                            )
                            
        elif select_input.startswith('DCSP_'):
            if validate_float(energy, theta, phi) and validate_int(int_z_or_comp) or validate_str(int_z_or_comp):
                output = calc_output(select_input, int_z_or_comp, energy, theta, phi)
                code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, theta, phi)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,
                            units = Request_Units.DCS_u,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            error = Request_Error.error
                            )
                                                
        elif select_input.startswith('Fi'):
            if validate_int(int_z) or validate_str(int_z) and validate_float(energy):
                output = calc_output(select_input, int_z, energy)
                code_examples = code_example(form.examples.choices, select_input, int_z, energy)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            error = Request_Error.error
                            )
        
        elif select_input == 'CosKronTransProb':
            if validate_int(int_z) or validate_str(int_z):
                output = calc_output(select_input, int_z, cktrans)
                code_examples = code_example(form.examples.choices, select_input, int_z, cktrans)
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            output = output,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, 
                            version = version, 
                            error = Request_Error.error
                            )
        
        elif select_input == 'ComptonProfile':
            if validate_float(pz) and validate_int(int_z) or validate_str(int_z):

                output = calc_output(select_input, int_z, pz)
                code_examples = code_example(form.examples.choices, select_input, int_z, pz)
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            output = output,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            error = Request_Error.error
                            )
        
        elif select_input == 'ComptonProfile_Partial':
            if validate_float(pz) and validate_int(int_z) or validate_str(int_z):
                output = calc_output(select_input, int_z, shell, pz)
                code_examples = code_example(form.examples.choices, select_input, int_z, shell, pz)
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            output = output,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            error = Request_Error.error
                            )
                            
        elif select_input == 'MomentTransf':
            if validate_float(energy, theta) == True:
                output = calc_output(select_input, energy, theta)
                code_examples = code_example(form.examples.choices, select_input, energy, theta)
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            output = output,  
                            code_examples = code_examples
                            )
            else:
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            error = Request_Error.error
                            )                    
        
        elif select_input == 'Refractive_Index':

            # Special Case: Refractive_Index input needs to be const char compound
            if validate_float(energy, density) and validate_int(int_z_or_comp) or validate_str(int_z_or_comp):
                try:
                    output = xraylib.Refractive_Index(
                        xraylib.AtomicNumberToSymbol(int(int_z_or_comp), 
                        float(energy), 
                        float(density)))
                    code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, density)
                    return render_template(
                        'index.html',
                        form = form, version = version,  
                        output = output, 
                        code_examples = code_examples
                        )
                except:
                    output = xraylib.Refractive_Index(
                        int_z_or_comp, 
                        float(energy), 
                        float(density))
                    code_examples = code_example(form.examples.choices, select_input, int_z_or_comp, energy, density)
                    return render_template(
                        'index.html',
                        form = form, version = version,  
                        output = output, 
                        code_examples = code_examples
                        )
                else:
                    return render_template(
                        'index.html', 
                        form = form, version = version,   
                        error = Request_Error.error
                        )                
            else:
                     return render_template(
                        'index.html', 
                        form = form, version = version,   
                        error = Request_Error.error
                        )
        
        elif select_input == 'CompoundParser':
            # Special Case: CompoundParser input needs to be const char compound
            if validate_str(comp):
                try:
                    out = xraylib.CompoundParser(str(comp))
                    
                    # Format output
                    w_fracts = out['massFractions']
                    w_pers = [str(round(i*100, 2)) + ' %' for i in w_fracts]
                    z = out['Elements']
                    sym = [ '<sub>' + str(i) + '</sub>' 
                        + str(xraylib.AtomicNumberToSymbol(i)) 
                        for i in z]
                    mmass = str(out['molarMass']) + ' g mol<sup>-1</sup>'
                    
                    output = {'Elements': sym, 
                        'Weight Fraction': w_pers, 
                        'Number of Atoms': out['nAtoms'], 
                        ' Molar Mass': mmass}
                    code_examples = code_example(form.examples.choices, select_input, comp)
                    return render_template(
                            'index.html', 
                            form = form, version = version, 
                            output = output,  
                            code_examples = code_examples, 
                            units = Request_Units.per_u
                            )
                except:
                    return render_template(
                            'index.html', 
                            form = form, version = version, 
                            error = Request_Error.error
                            )  
            else:
                return render_template(
                            'index.html', 
                            form = form, version = version, 
                            error = Request_Error.error
                            )                    
                                                                                        
        elif select_input == 'GetRadioNuclideDataList':
            output = xraylib.GetRadioNuclideDataList()
            output.insert(0, '<b> Radionuclides: </b>')
            output = '<br/>'.join(output) 
            code_examples = code_example(form.examples.choices, select_input)
            return render_template(
                    'index.html',  
                    form = form, version = version, 
                    output = output, 
                    code_examples = code_examples
                    )
        
        elif select_input == 'GetRadioNuclideDataByIndex':
            out = calc_output(select_input, rad_nuc)
            print(out)
            # Format output
            line_nos = out['XrayLines']           
            x_energy = [xraylib.LineEnergy(out['Z_xray'], i) for i in line_nos]
            
            output = {'X-ray Energies': x_energy, 
                'Disintegrations s<sup>-1</sup>': out['XrayIntensities'], 
                'Gamma-ray Energy': out['GammaEnergies'], 
                'Disintegrations s<sup>-1</sup> ': out['GammaIntensities']}
            code_examples = code_example(form.examples.choices, 'GetRadioNuclideDataByName', rad_nuc)
            
            return render_template(
                    'index.html',  
                    form = form, 
                    version = version, 
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
                    version = version, 
                    output = output, 
                    code_examples = code_examples
                    )
                    
        elif select_input == 'GetCompoundDataNISTByIndex':
            out = calc_output(select_input, nistcomp)
            
            # Format output
            w_fracts = out['massFractions']
            w_pers = [str(round(i*100, 2)) + ' %' for i in w_fracts]
            z = out['Elements']
            sym = [ '<sub>' + str(i) + '</sub>' 
                + str(xraylib.AtomicNumberToSymbol(i)) 
                for i in z]
            density = str(out['density']) + ' g cm<sup>-3</sup>'
                    
            output = {'Elements': sym, 'Weight Fraction': w_pers, ' Density': density}           
            code_examples = code_example(form.examples.choices, 'GetCompoundDataNISTByName', nistcomp)
            return render_template(
                    'index.html',
                    form = form, 
                    version = version,  
                    output = output,
                    code_examples = code_examples
                    )               

    return render_template('index.html', form=form, version = version)                        
                
