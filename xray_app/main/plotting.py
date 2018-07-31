from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import xraylib 
fig = Figure() #Figure is the final image which may contain 1 or more Axes. 

# A canvas must be manually attached to the figure (pyplot would automatically
# do it).  This is done by instantiating the canvas with the figure as
# argument.
FigureCanvas(fig)

# Axes represent an individual plot (don’t confuse this with the word “axis”, which refers to the x/y axis of a plot)

x = []
y = []

def graph_data():   
    for i in range(1, 20, 1):
        x.append(i)
        y.append(xraylib.ElementDensity(i)) #change to elementdensity

def print_data(*lsts):
    lst = zip(*lsts)    
    for value in lst:
        print(value)
    
graph_data()
print_data(x, y)

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x, y, label='ElementDensity')
ax.set(xlabel='Element', ylabel='Density')

ax.legend()
fig.savefig('elementdensity.png', dpi=80)

plt.show()
