from timbre import *
import numpy as np

__all__ = ['Even','Odd','Evenodd','Square','Sawtooth','Triangle','Custom','Beam']

class Even(Timbre):
    """A Timbre object with Even harmonics.
    """
    def __init__(self, f_0 = 220, numPartials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, numPartials)
        self.attenuation = attenuation
        self.freqs = [self.f_0 * i for i in range(1, 2 * self.numPartials) if i == 1 or i % 2 == 0]
        self.amps = [self.attenuation**p for p in range(self.numPartials)]
        self.harmonics = 'EvenHarmonics'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.numPartials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.numPartials)

class Odd(Timbre):
    """A Timbre object with Odd harmonics
    """
    def __init__(self, f_0 = 220, numPartials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, numPartials)
        self.attenuation = attenuation
        self.freqs = [self.f_0 * i for i in range(1, 2 * self.numPartials + 1) if i % 2 != 0]
        self.amps = [self.attenuation**p for p in range(self.numPartials)]
        self.harmonics = 'OddHarmonics'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.numPartials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.numPartials)


class Evenodd(Timbre):
    """A Timbre object with Even and Odd harmonics
    """
    def __init__(self, f_0 = 220, numPartials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, numPartials)
        
        self.attenuation = attenuation
        self.freqs = [self.f_0 * i for i in range(1, self.numPartials + 1)]
        self.amps = [self.attenuation**p for p in range(self.numPartials)]
        self.harmonics = 'EvenOddHarmonics'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.numPartials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.numPartials)


class Square(Timbre):
    """A Timbre object with A Square wave (additive synthesis). Odd Harmonics. Attenuation rate is fixed at 1 / n 
    """
    def __init__(self, f_0 = 220, numPartials = 7):
        Timbre.__init__(self, f_0, numPartials)
        self.freqs = [self.f_0 * i for i in range(1, 2 * self.numPartials + 1) if i % 2 != 0]
        self.amps = [1.0/(i) for i in range(1, 2 * self.numPartials + 1) if i % 2 != 0]
        self.harmonics = 'SquareWave'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.numPartials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.numPartials)



class Sawtooth(Timbre):
    """A Timbre object with A Sawtooth wave (additive synthesis). Attenuation rate is fixed at 2*(-1^n)/n * pi, n being the partial #
    """
    def __init__(self, f_0 = 220, numPartials = 7):
        Timbre.__init__(self, f_0, numPartials)
        self.freqs = [self.f_0 * i for i in range(1, self.numPartials + 1)]
        self.amps = [2*((-1)**i)/(np.pi * i) for i in range(1, self.numPartials + 1)]
        print self.amps
        self.harmonics = 'SawtoothWave'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.numPartials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.numPartials)



class Triangle(Timbre):
    """A Timbre object with A Triangle wave (additive synthesis). Attenuation rate is fixed at 0.8105694691387022*((-1)^((n - 1)/2.)/(n^2)) n being the partial #
    """
    def __init__(self, f_0 = 220, numPartials = 7):
        Timbre.__init__(self, f_0, numPartials)
        self.freqs = [self.f_0 * i for i in range(0, 2 * self.numPartials + 1) if i % 2 != 0]
        self.amps = [0.8105694691387022*((-1)**((i - 1)/2.)/(i**2)) for i in range(1, 2 * self.numPartials + 1) if i % 2 != 0]
        self.harmonics = 'TriangleWave'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.numPartials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.numPartials)

class Custom(Timbre):
    """A Timbre object with Custom harmonics.
    
            * freq_array: an array of frequencies
            * amps_array: an array of amplitides
            * freq_array and amps_array must have the same length
    """
    def __init__(self, freq_array, amps_array): #phaseArray, env_array - used with fft.py
        f_0 = min(freq_array)
        numPartials = len(freq_array)
        Timbre.__init__(self, f_0, numPartials)
        self.f_O = f_0
        self.numPartials = numPartials
        self.freqs = freq_array
        self.amps = amps_array
        # self.phase = phaseArray
        self.harmonics = 'CustomHarmonics'
        # self.env = env_array
        
        print "Timbre successfully initialized with custom partials"

class Beam(Timbre):
    """A Timbre object with Beam harmonics. Partial frequencies are .4413 * f_0*(n +.5)^2
    """
    def __init__(self, f_0 = 220, numPartials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, numPartials)
        self.attenuation = attenuation
        self.freqs = [.4413 * f_0*(n +.5)**2 for n in range(1, numPartials + 1)]
        self.amps = [self.attenuation**p for p in range(numPartials)]
        self.harmonics = 'BeamHarmonics'
        print "Timbre successfully initialized with Beam partials"
    
