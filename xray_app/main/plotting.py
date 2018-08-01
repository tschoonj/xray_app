
    
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams.update({'figure.autolayout': True})


def make_fig(x, y):
    fig = Figure()
    FigureCanvas(fig)
    fig, ax = plt.subplots()
    ax.plot(x, y, label='ElementDensity')
    ax.set(xlabel='Element', ylabel='Density')
    ax.legend()
    fig.savefig('elementdensity.png', dpi=80)

    plt.show()
