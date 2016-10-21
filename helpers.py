from timbre import *
from generators import *
import matplotlib.pyplot as plt
import numpy as np
__all__ = ['plotMultiple', 'disPlotMultiple']


def disPlotMultiple(*args):
    """Plots the dissonance curves for multiple Timbre objects. Uses the non-normalized dissonance arrays to allow for comparison 
    
        Usage:
    
            >>> disPlotMultiple(foo, bar, baz)
    """
    ymax = []
    octavesMax = []
    widthMax = []
    for arg in args:
        ymax.append(max(arg.dissonances))
        octavesMax.append(arg.octaves)
        widthMax.append(arg.width)
        plt.plot(np.arange(1,arg.octaves, arg.increment),arg.dissonances, linewidth=1.0, label = '%s harmonics\n%d Hz f_0\n%d partials' % (arg.name, arg.f_0, arg.n_partials))
        plt.legend()
    plt.axis([1,max(octavesMax),0,max(ymax)])
    plt.subplots_adjust(bottom=.2)
    labels = [str(n) for n in range(len(np.arange(0,max(widthMax) + 1./12,1./12)))]
    plt.xticks([2**i for i in np.arange(0,max(widthMax) + 1./12,1./12)],labels) # set ticks at equal tempered intervals
    plt.xlabel('Semitone Intervals (12TET)')
    plt.ylabel('Relative Dissonance')
    leg = plt.legend(fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.grid(True)
    plt.show()



"""
import Timbre
foo = Timbre.Even()
foo.disMeasure()
bar = Timbre.Odd()
bar.disMeasure()
disPlotMultiple(foo, bar)

"""