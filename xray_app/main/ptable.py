# Periodic Table built using xraylib
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Legend
from bokeh.transform import dodge, factor_cmap

import xraylib
import numpy as np

# Defining lists and arrays
y = []
tools = 'hover, pan, zoom_in, reset'
tooltips = [
    ("Density", "@density"),
    ("Abs. Edge Energy", "@absedge"),
    ("Atomic Level Width", "@alw"),
    ("Fluorescence Yield", "@flyield"),
    ("AugerYield", "@augyield")
]
cmap = {
    "alkali metal": "#a6cee3",
    "alkaline earth metal": "#78aed2",
    "metal": "#5f0f40",
    "halogen": "#40b5bb",
    "metalloid": "#e0777d",
    "noble gas": "#5b54a2",
    "nonmetal": "#a4508b",
    "transition metal": "#ade25d",
    "lanthanide actinide": "#ffdd56",
}
periods = ["I", "II", "III", "IV", "V", "VI", "VII", "", " ", "   "]
groups = [str(x) for x in range(1, 19)]

group1 = np.array([1, 3, 11, 19, 37, 55, 87])
group2 = np.array([4, 12, 20, 38, 56, 88])
group3 = np.array([21, 39])
group4 = np.array([22, 40, 72, 104])
group5 = group4 + 1
group6 = group5 + 1
group7 = group6 + 1
group8 = group7 + 1
group9 = group8 + 1
group10 = group9 + 1
group11 = group10 +1
group12 = group11 + 1
group13 = np.array([5, 13, 31, 49, 81, 113])
group14 = group13 + 1
group15 = group14 + 1
group16 = group15 + 1
group17 = group16 + 1
group18 = np.array([2, 10, 18, 36, 54, 86, 118])
ln = np.arange(57, 72)
ac = np.arange(89, 104)

alkali_metal = group1[1:]
alkaline_earth_metal = group2
t_metal = np.concatenate((group3, group4, group5, group6, group7, group8, group9, group10, group11, group12))
halogen = group17
metal = np.array([13, 31, 49, 81, 50, 82, 83, 84])
metalloid = np.array([5, 14, 32, 33, 51, 52, 85])
noble_gas = group18
nonmetal = np.array([1, 6, 7, 8, 9, 15, 16, 17, 34, 35, 53])
ln_ac = np.concatenate((ln, ac))

# Query xraylib and formats data into ColumnDataSource format
def get_data():
    sym, z, group, period, _type = ([], [], [], [], [])
    mass, density, absedge, alw, flyield, augyield = ([], [], [], [], [], [])
    for i in range(1, 104):
        s = xraylib.AtomicNumberToSymbol(i)
        sym.append(s)
        z.append(i)
        mass.append(xraylib.CompoundParser(s)['molarMass'])
        density.append(str(xraylib.ElementDensity(i)) + ' g/cm^3')
        
        absedge.append(str(xraylib.EdgeEnergy(i, 0)) + ' keV')        
        alw.append(str(xraylib.AtomicLevelWidth(i, 0)) + ' keV')
        flyield.append(str(xraylib.FluorYield(i, 0)))
        augyield.append(str(xraylib.AugerYield(i, 0)))
        
        pop_period(i, period)
        pop_group(i, group)
        pop_type(i, _type)
        
    data = {'sym': sym, 'z': z, 'mass': mass, 'group':group, 'period':period, '_type': _type, 'density': density, 'flyield': flyield, 'augyield': augyield, 'absedge': absedge, 'alw': alw}
    #print(data)
    return data

# Populating keys needed for formatting 
def pop_type(i, _type):
    if i in alkali_metal:
        _type.append('alkali metal')
    elif i in alkaline_earth_metal:
        _type.append('alkaline earth metal')
    elif i in t_metal:
        _type.append('transition metal')
    elif i in halogen:
        _type.append('halogen')
    elif i in metal:
        _type.append('metal')
    elif i in metalloid:
        _type.append('metalloid')
    elif i in noble_gas:
        _type.append('noble gas')
    elif i in nonmetal:
        _type.append('nonmetal')
    elif i in ln_ac:
        _type.append('lanthanide actinide')
        
def pop_group(i, group):
    if i in group1:
        group.append(groups[0])
    elif i in group2:
        group.append(groups[1])
    elif i in group3:
        group.append(groups[2])
    elif i in group4:
        group.append(groups[3])
    elif i in group5:
        group.append(groups[4])
    elif i in group6:
        group.append(groups[5])
    elif i in group7:
        group.append(groups[6])
    elif i in group8:
        group.append(groups[7])
    elif i in group9:
        group.append(groups[8])
    elif i in group10:
        group.append(groups[9])
    elif i in group11:
        group.append(groups[10])
    elif i in group12:
        group.append(groups[11])
    elif i in group13:
        group.append(groups[12])
    elif i in group14:
        group.append(groups[13])
    elif i in group15:
        group.append(groups[14])
    elif i in group16:
        group.append(groups[15])
    elif i in group17:
        group.append(groups[16])
    elif i in group18:
        group.append(groups[17])
    elif i in ln or i in ac:
        if i == 57 or i == 89:
            group.append(groups[3])
        elif i == 58 or i == 90:
            group.append(groups[4])
        elif i == 59 or i == 91:
            group.append(groups[5])
        elif i == 60 or i == 92:
            group.append(groups[6])
        elif i == 61 or i == 93:
            group.append(groups[7])
        elif i == 62 or i == 94:
            group.append(groups[8])
        elif i == 63 or i == 95:
            group.append(groups[9])
        elif i == 64 or i == 96:
            group.append(groups[10])
        elif i == 65 or i == 97:
            group.append(groups[11])
        elif i == 66 or i == 98:
            group.append(groups[12])
        elif i == 67 or i == 99:
            group.append(groups[13])
        elif i == 68 or i == 100:
            group.append(groups[14])
        elif i == 69 or i == 101:
            group.append(groups[15])
        elif i == 70 or i == 102:
            group.append(groups[16])
        elif i == 71 or i == 103:
            group.append(groups[17])
                
def pop_period(i, period):
    if i in range(1, 3):
        period.append(periods[0])
    elif i in range(3, 11):
        period.append(periods[1])
    elif i in range(11, 19):
        period.append(periods[2])
    elif i in range(19, 37):
        period.append(periods[3])
    elif i in range(37, 55):
        period.append(periods[4])
    elif i in range(55, 57) or i in range(72, 87):
        period.append(periods[5])
    elif i in range(87, 89):
        period.append(periods[6])
    elif i in range(57, 72):
        period.append(periods[7])
    elif i in range(89, 104):     
        period.append(periods[8])

# Creates Bokeh object and formats it                         
def create_table():
    data = ColumnDataSource(data=get_data())
    table = figure(title = 'Periodic Table Widget', plot_width = 1000, plot_height=600, x_range = groups, y_range = list(reversed(periods)), tools = tools, tooltips = tooltips, sizing_mode='scale_width', x_axis_location = "above")
    
    table.rect('group','period', 0.93, 0.93, fill_alpha = 0.7, muted_alpha=0.2,
            source = data, legend = '_type', 
            color = factor_cmap('_type', palette = list(cmap.values()), factors = list(cmap.keys())), 
            muted_color = factor_cmap('_type', palette = list(cmap.values()), factors = list(cmap.keys())))
    #  to add a legend to the table
    
    txt_format = {"source": data, "text_align": "left", "text_baseline": "middle"}
    x = dodge("group", -.3, range = table.x_range)
    
    txt = table.text(x = x, y = "period", text = "sym", **txt_format)
    txt.glyph.text_font_style="bold"
    txt.glyph.text_font_size = "1em"
    
    txt = table.text(x = x, y = dodge("period", 0.25, range = table.y_range), 
            text = "z", **txt_format)
    txt.glyph.text_font_size = "0.8em"
    
    txt = table.text(x = x, y = dodge("period", -0.2, range = table.y_range), 
            text = "mass", **txt_format)
    txt.glyph.text_font_size = "0.7em"
    
    table.text(x=["3", "3"], y=["VI", "VII"], text=["57-71", "89-103"], text_align="center", text_baseline="middle", text_font_size = "0.7em")
    table.outline_line_color = None
    table.grid.grid_line_color = None
    table.axis.axis_line_color = None
    table.axis.major_tick_line_color = None
    
    table.legend.orientation = "horizontal"
    table.legend.location ="bottom_center"
    return table
