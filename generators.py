from timbre import *
import numpy as np

__all__ = ['Even','Odd','Evenodd','Square','Sawtooth','Triangle','Custom','Beam']

class Even(Timbre):
    """A Timbre object with Even harmonics.
    """
    def __init__(self, f_0 = 220, n_partials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, n_partials)
        self.attenuation = attenuation
        self.freqs = [self.f_0*i for i in range(1,2*self.n_partials) if i == 1 or i % 2 == 0]
        self.amps = [self.attenuation**p for p in range(self.n_partials)]
        self.harmonics = 'Even Harmonics'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.n_partials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.n_partials)

class Odd(Timbre):
    """A Timbre object with Odd harmonics
    """
    def __init__(self,f_0 = 220, n_partials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, n_partials)
        self.attenuation = attenuation
        self.freqs = [self.f_0*i for i in range(1,2*self.n_partials + 1) if i % 2 != 0]
        self.amps = [self.attenuation**p for p in range(self.n_partials)]
        self.harmonics = 'Odd Harmonics'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.n_partials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.n_partials)


class Evenodd(Timbre):
    """A Timbre object with Even and Odd harmonics
    """
    def __init__(self, f_0 = 220, n_partials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, n_partials)
        
        self.attenuation = attenuation
        self.freqs = [self.f_0*i for i in range(1,self.n_partials + 1)]
        self.amps = [self.attenuation**p for p in range(self.n_partials)]
        self.harmonics = 'Even and Odd Harmonics'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.n_partials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.n_partials)


class Square(Timbre):
    """A Timbre object with A Square wave (additive synthesis). Odd Harmonics. Attenuation rate is fixed at 1/n 
    """
    def __init__(self,f_0 = 220, n_partials = 7):
        Timbre.__init__(self, f_0, n_partials)
        self.freqs = [self.f_0*i for i in range(1,2*self.n_partials + 1) if i % 2 != 0]
        self.amps = [1.0/(i) for i in range(1,2*self.n_partials + 1) if i % 2 != 0]
        self.harmonics = 'Square Wave'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.n_partials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.n_partials)



class Sawtooth(Timbre):
    """A Timbre object with A Sawtooth wave (additive synthesis). Attenuation rate is fixed at 2*(-1^n)/n*pi, n being the partial #
    """
    def __init__(self,f_0 = 220, n_partials = 7):
        Timbre.__init__(self, f_0, n_partials)
        self.freqs = [self.f_0*i for i in range(1,self.n_partials + 1)]
        self.amps = [2*((-1)**i)/(np.pi*i) for i in range(1, self.n_partials + 1)]
        self.harmonics = 'Sawtooth Wave'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.n_partials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.n_partials)



class Triangle(Timbre):
    """A Timbre object with A Triangle wave (additive synthesis). Attenuation rate is fixed at 0.8105694691387022*((-1)^((n-1)/2.)/(n^2)) n being the partial #
    """
    def __init__(self,f_0 = 220, n_partials = 7):
        Timbre.__init__(self, f_0, n_partials)
        self.freqs = [self.f_0*i for i in range(0,2*self.n_partials + 1) if i % 2 != 0]
        self.amps = [0.8105694691387022*((-1)**((i-1)/2.)/(i**2)) for i in range(1, 2*self.n_partials + 1) if i % 2 != 0]
        self.harmonics = 'Triangle Wave'
        if hasattr(self, 'attenuation'):
            print "Timbre successfully initialized with parameters of %dHz, %d partials, attenuation factor of %.2f\n" % (self.f_0, self.n_partials, self.attenuation)
        else:
            print "Timbre successfully initialized with parameters of %dHz, %d partials\n" % (self.f_0, self.n_partials)

class Custom(Timbre):
    """A Timbre object with Custom harmonics.
    
            * freq_array: an array of frequencies
            * amps_array: an array of amplitides
            * freq_array and amps_array must have the same length
    """
    def __init__(self, freq_array, amps_array, phaseArray, env_array):
        f_0 = min(freq_array)
        n_partials = len(freq_array)
        Timbre.__init__(self, f_0, n_partials)
        self.f_O = f_0
        self.n_partials = n_partials
        self.freqs = freq_array
        self.amps = amps_array
        self.phase = phaseArray
        self.harmonics = 'custom harmonics'
        self.env = env_array
        
        print "Timbre successfully initialized with custom partials"

class Beam(Timbre):
    """A Timbre object with Beam harmonics. Partial frequencies are .4413*f_0*(n +.5)^2
    """
    def __init__(self,f_0 = 220, n_partials = 7, attenuation = .7071):
        Timbre.__init__(self, f_0, n_partials)
        self.attenuation = attenuation
        self.freqs = [.4413*f_0*(n +.5)**2 for n in range(1,n_partials + 1)]
        self.amps = [self.attenuation**p for p in range(n_partials)]
        self.harmonics = 'beam harmonics'
        print "Timbre successfully initialized with Beam partials"
    
