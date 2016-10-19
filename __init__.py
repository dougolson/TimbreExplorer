# -*- coding: utf-8 -*-
"""
The Timbre Explorer module creates Timbre objects for the investigation of the dissonance and consonance properties of musical timbres. The disMeasure() function
is a Python translation of `William Sethares's matlab and C code <http://sethares.engr.wisc.edu/comprog.html>`_. I have added
functions to do plots of various kinds and to generate .wav files so you can hear the timbres and their dissonance / consonance patterns. Requires Matplotlib, Numpy and Scipy.

Objects can be initialized as:
    * Even
    * Odd
    * Evenodd
    * Square
    * Sawtooth
    * Triangle
    * Beam
    * Custom

Most objects have the following properties:

    * **f_0**: the fundamental frequency. Default is 220 Hz
    * **n_partials**: the desired number of partials in the tone. Default is 7
    * **attenuation**: the attenuation rate to be applied to the partials. Default is .7071

Specific waveforms such as Square, Sawtooth etc, have predefined spectra and attenuation rates

The Custom object allows the user to specify any desired set of partials and amplitudes.

Typical usage, assuming you cd to the directory that contains the **Timbre** directory and run Python 2.7x from there:

    >>> import Timbre
    >>> foo = Timbre.Even()
    >>> foo.disMeasure(octaves = 1) # perform the dissonance calculation
    >>> foo.disPlot() # plot the dissonance curve for the timbre
    >>> foo.ConsDisFreqs() # plot of the maximima and minima in the dissonance curve
    >>> foo.partialsPlot() # bar plot of the relative amplitudes and frequencies for the partials of the timbre 
    >>> foo.wavePlot() # plot one period of the timbre's waveform
    >>> foo.timbreGen() # Generate a 5 second sample of the timbre 
    >>> foo.timbreSweep(length = 60) # Generate a sweep of the timbre against itself
    >>> bar = Timbre.Beam()
    >>> Timbre.disPlotMultiple(foo, bar) # Generate a dissonance plot for both foo and bar



"""
import Timbre.timbre
from Timbre.helpers import *
from Timbre.generators import *
