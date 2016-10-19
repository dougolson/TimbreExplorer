
# Timbre Explorer

The Timbre Explorer module creates Timbre objects for the investigation of the dissonance and consonance properties of musical timbres. The disMeasure() function is not mine - it is a Python translation of [William Sethares’s matlab and C code](http://sethares.engr.wisc.edu/comprog.html). I have added functions to do plots of various kinds and to generate .wav files so you can hear the timbres and their dissonance / consonance patterns. Requires Matplotlib, Numpy and Scipy.


```python
import Timbre
import matplotlib.pyplot as plt
```


```python
%matplotlib inline
plt.rcParams['figure.figsize'] = (10, 6)
```

Typical usage, assuming you cd to the directory that contains the Timbre directory and run Python 2.7x from there:
* import Timbre
* foo = Timbre.Even()
* foo.disMeasure(octaves = 1) # perform the dissonance calculation
* foo.disPlot() # plot the dissonance curve for the timbre
* foo.ConsDisFreqs() # plot of the maximima and minima in the dissonance curve
* foo.partialsPlot() # bar plot of the relative amplitudes and frequencies for the partials of the timbre 
* foo.wavePlot() # plot one period of the timbre's waveform
* foo.timbreGen() # Generate a 5 second sample of the timbre 
* foo.timbreSweep(length = 60) # Generate a sweep of the timbre against itself

Create some Timbre objects. Objects can be initialized as:
 * Even (even partials)
 * Odd (odd partials)
 * Evenodd (even and odd partials etc.)
 * Square 
 * Sawtooth
 * Triangle
 * Beam
 * Custom


```python
even = Timbre.Even()
odd = Timbre.Odd()
beam = Timbre.Beam()
```

    Timbre successfully initialized with parameters of 220Hz, 7 partials, attenuation factor of 0.71
    
    Timbre successfully initialized with parameters of 220Hz, 7 partials, attenuation factor of 0.71
    
    Timbre successfully initialized with Beam partials


Run the disMeasure analysis:


```python
even.disMeasure()
odd.disMeasure()
beam.disMeasure()
```

Make some plots:


```python
even.disPlot()
```


![png](/Doc/overview/output_9_0.png)


Note the flat third (interval 4) 


```python
odd.disPlot()
```


![png](/Doc/overview/output_11_0.png)



```python
beam.disPlot()
```


![png](/Doc/overview/output_12_0.png)


Note the stetched partials of the vibrating beam timbre, especially the sixth and octave


```python
Timbre.disPlotMultiple(even, odd, beam)
```


![png](/Doc/overview/output_14_0.png)



```python
square = Timbre.Square(n_partials = 25)
```

    Timbre successfully initialized with parameters of 220Hz, 25 partials
    



```python
square.wavePlot()
```


![png](/Doc/overview/output_16_0.png)



```python
square.partialsPlot()
```


![png](/Doc/overview/output_17_0.png)



```python
square.disMeasure()
square.disPlot()
```


![png](/Doc/overview/output_18_0.png)



```python

```
