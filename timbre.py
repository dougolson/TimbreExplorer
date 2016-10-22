
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import argrelextrema


__all__ = ['Timbre']

class Timbre(object):
    """Parent class for the various timbre objects. Use subclasses Even, Odd, Evenodd, Square, Sawtooth, Triangle, Beam and Custom to create objects"""
    def __init__(self, f_0, numPartials,octaves = 1):
        self.name = type(self).__name__
        self.increment = .01
        self.f_0 = f_0
        self.numPartials = numPartials
        
    def audioGenPath(self):
        if not os.path.exists('TimbreAudio'):
            os.makedirs('TimbreAudio')
        
    def disMeasure(self, octaves = 1):
        """Calculates the relative dissonance for a given Timbre object at all intervals within a specified range. disMeasure(octaves = 1).

        returns an an array of relative dissonances **self.dissonances** and a normalized dissonance array **self.norm**

        """
        self.width = octaves
        self.octaves = 2**octaves + .3 # - octaves + 2
        # Parameters
        Dstar = 0.24
        S1 = 0.0207
        S2 = 18.96
        C1 = 5
        C2 = -5
        A1 = -3.51
        A2 = -5.75
        inc = self.increment # step increment for x values
        frequencies = self.freqs
        amplitudes = [abs(amp) for amp in self.amps]
        dissonances = [] # empty array for i loop
        x1 = zip(frequencies,amplitudes)
        for i in np.arange(1,self.octaves, inc):
            x2 = [freq*i for freq in frequencies] # iterate each frequency in the frequency array over the x increments
            x2 = zip(x2,amplitudes) # zip each frequency with its associated amplitude
            diss_j = [] # empty array for j loop
            for j in x1:
                diss_k = [] # empty array for k loop
                for k in x2: #perform calculations on each element of x2 and append result to diss_k array
                    S=Dstar/(S1*min(j[0],k[0]) + S2)
                    Fdif = abs(k[0] - j[0])
                    a = min(j[1],k[1])
                    diss_k.append(a*(C1*np.e**(A1*S*Fdif)+C2*np.e**(A2*S*Fdif)))
                diss_j.append(np.sum(diss_k)) # sum each k iteration and append to j array
            dissonances.append(np.sum(diss_j)) # sum each j iteration and append to dissonances array
        normalizedDissonances = [diss/max(dissonances) for diss in dissonances] # normalize
        self.dissonances = dissonances # add raw values to self
        self.normalizedDissonances = normalizedDissonances # add normalized values to self

    def disPlot(self, normalized = True):
        """Plots relative dissonance at all intervals for a given tone"""
        if not hasattr(self,'normalizedDissonances'):
            self.disMeasure()
        if normalized:
            plt.plot(np.arange(1,self.octaves, self.increment),self.normalizedDissonances)
        else:
            plt.plot(np.arange(1,self.octaves, self.increment),self.dissonances)
        plt.axis([1,self.octaves,0,1.1])
        plt.subplots_adjust(bottom=.2)
        labels = [str(n) for n in range(len(np.arange(0,self.width + 1./12,1./12)))]
        plt.xticks([2**i for i in np.arange(0,self.width + 1./12,1./12)],labels) # set ticks at equal tempered intervals
        if hasattr(self, 'attenuation'):
            plt.suptitle('%s Hz Fundamental, %d Partials, AttenRate %.2f, %s' % (self.f_0, self.numPartials, self.attenuation, self.harmonics), fontsize = 12)
        else:
            plt.suptitle('%s Hz Fundamental, %d Partials, %s' % (self.f_0, self.numPartials,self.harmonics), fontsize = 12)
        roundFreqs = [round(f,2) for f in self.freqs]
        if len(roundFreqs) > 9:
            roundFreqs = roundFreqs[:9]
            roundFreqs.append('etc')
        plt.title('Frequencies: ' + str(roundFreqs), fontsize = 12)
        plt.xlabel('Semitone Interval (12TET)')
        plt.ylabel('Relative Dissonance')
        plt.grid(True)
        plt.show()
        
            

    def partialsPlot(self):
        """Plots the partials and their relative amplitudes for the timbre being examined. Positive Amplitudes in red, Negative amplitudes in blue."""
        wdth = self.f_0/4.0
        plt.bar(self.freqs,self.amps, width = wdth, color = 'r')
        for freq,amp in zip(self.freqs, self.amps):
            if amp < 0:
                plt.bar(freq, abs(amp),width = wdth, color = 'b')
        plt.xticks(self.freqs, rotation = 45)
        plt.axis([min(self.freqs)-wdth,max(self.freqs)+2*wdth,0, 1.1])
        plt.ylabel('Relative Amplitude')
        plt.xlabel('Frequency in Hz')
        plt.title('Partials for %s Object' % self.name)
        plt.subplots_adjust(bottom=0.15)
        plt.show()

    def wavePlot(self):
        """Generates a plot of the waveform for the timbre being examined"""
        inc = .01/max(self.freqs)
        T = 1./min(self.freqs)
        x = np.arange(0,T*1.01, T/100.0)
        data = np.zeros(len(x))
        for f,a in zip(self.freqs,self.amps):
            y = a*np.sin(2*np.pi*f*x)
            data = np.sum([data,y], axis = 0)
        self.data = [d/max(abs(data)) for d in data]
        plt.plot(self.data, label = '%s harmonics\nf_0 = %d Hz\n%d partials' % (self.name, self.f_0, self.numPartials))
        plt.axis([0,100,-1.1,1.1])
        labels = [str(round(1000*n,2)) for n in np.arange(0,T*1.01,T/10.0)]
        plt.xticks([n for n in np.arange(0, 101, 10)], labels)
        leg = plt.legend(fancybox=True)
        leg.get_frame().set_alpha(0.5)
        plt.xlabel('Milliseconds')
        plt.title('Waveform of %s Object' % self.name)
        plt.grid(True)
        plt.show()
        
    def consDisFreqs(self, makePlot = False):
        """
        Generates a list of the consonances (minima on the dissonance plot) for a given timbre. The consonances are used by consFreqs and writeChord. Optionally plots a bar graph                  showing the peak dissonant an consonant frequencies for a given Timbre object
        """
        if not hasattr(self,'normalizedDissonances'):
            self.disMeasure()
        x = np.asarray(self.normalizedDissonances)
        dis = argrelextrema(x, np.greater)
        self.dissonances = [self.f_0*(1 + d*self.increment) for d in dis]
        con = argrelextrema(x, np.less)
        self.dissonances = self.dissonances[0]
        self.consonances = [self.f_0*(1 + c*self.increment) for c in con]
        self.consonances = self.consonances[0]
        if makePlot:
            hDis = np.ones(len(self.dissonances))
            hCon = np.ones(len(self.consonances))
            ticks = np.append(self.consonances, self.dissonances)
            plt.bar(np.round(self.consonances,2),hCon,max(ticks)/200.0, color = 'b', align = 'center', label = 'Consonant')
            plt.bar(np.round(self.dissonances,2),hDis,max(ticks)/200.0, color = 'r', align='center', label = 'Dissonant')
            plt.xticks(ticks, rotation = 90, fontsize = 10)
            leg = plt.legend(fancybox=True)
            leg.get_frame().set_alpha(0.75)
            plt.show()

    def consFreqs(self, makePlot = False):
        """Generates an array of consonant frequencies for a given Timbre. Optionally plots a bar graph showing the peak dissonant an consonant frequencies for a given Timbre object"""
        if not hasattr(self,'normalizedDissonances'):
            self.disMeasure()
        x = np.asarray(self.normalizedDissonances)
        con = argrelextrema(x, np.less)
        self.consonances = [self.f_0*(1 + c*self.increment) for c in con]
        self.consonances = self.consonances[0]
        if makePlot:
            hCon = np.ones(len(self.consonances))
            ticks = self.consonances
            plt.bar(np.round(self.consonances,2),hCon,max(ticks)/500.0, color = 'b', align = 'center', label = 'Consonances for %d Hz Fundamental' % self.f_0)
            plt.xticks(ticks, rotation = 90, fontsize = 10)
            leg = plt.legend(fancybox=True)
            leg.get_frame().set_alpha(0.75)
            plt.show()

    def timbreGen(self):
        """Generates audio data and a .wav file of a timbre. 
               * Default length 5 seconds. 
               * files in TimbreAudio in cwd
        """
        self.audioGenPath()
        while True:
            length = raw_input("Enter file length in seconds: ")
            try:
                length = (int(length))
                break
            except ValueError:
                print "Value must be an integer"
        sampleInc = 1.0/44100
        # if hasattr(self, 'env'): # Used with fft.py
#             length = len(self.env)/44100.0
        x = np.arange(0,length, sampleInc)
        wavData = np.zeros(len(x))
        for i,(freq,amp) in enumerate(zip(self.freqs,self.amps)):
            # if hasattr(self, 'phase'): # Used with fft.py
            #     y = amp*np.sin(2*np.pi*freq*x + self.phase[i])
            # else:
                # y = amp*np.sin(2*np.pi*freq*x)
            y = amp*np.sin(2*np.pi*freq*x)
            wavData = np.sum([wavData,y], axis = 0)
        mx = 1.1*(max(abs(wavData)))
        wavData = np.asarray(wavData)
        wavData = wavData/mx
        # if hasattr(self, 'env'): # used with fft.py
#             wavData = self.env * wavData
        wavData = np.asarray(32000*wavData, dtype = np.int16)
        write('TimbreAudio/%dHz_%dpartials_%s.wav' % (self.f_0, self.numPartials, self.harmonics ), 44100.0, wavData)
        print "File written to TimbreAudio folder"


    def timbreSweep(self):
        """Generates audio data and a .wav file of a timbre swept against itself. One tone is held constant, the other ascends for just over 1 octave.
               * Default length 90 seconds. 
               * files in TimbreAudio in cwd
        """
        self.audioGenPath()
        while True:
            length = raw_input("Enter file length in seconds: ")
            try:
                length = (int(length))
                break
            except ValueError:
                print "Value must be an integer"
        sampleInc = 1.0/44100
        f_Start, f_Stop = self.freqs, [2.2*f for f in self.freqs] # 2 arrays, one of initial and one of final partials 
        times = np.arange(0, length, sampleInc) # array of chosen length at 44.1 kHz sample rate
        ramp = 1.*times/length # linear ramp 
        rampArray = [f0*(1-ramp) + f1*ramp for f0,f1 in zip(f_Start, f_Stop)] #generates an list of arrays, one for each frequency
        sweepData = np.zeros(len(times))
        phaseCorrect = [np.add.accumulate(times*np.concatenate((np.zeros(1), 2*np.pi*(x[:-1]-x[1:])))) for x in rampArray]
        for freq,amp in zip(self.freqs,self.amps): # Constant frequency
            y = amp*np.sin(2*np.pi*freq*times)
            sweepData = np.sum([sweepData,y], axis = 0)
        for array,amp,phase in zip(rampArray,self.amps,phaseCorrect): # swept frequency
            tempData = amp*np.sin(2*np.pi*array*times + phase)
            sweepData = np.sum([sweepData,tempData], axis = 0)
        mx = 1.1*(max(abs(sweepData)))
        sweepData = np.asarray(sweepData)
        sweepData = sweepData/mx
        sweepData = np.asarray(32000*sweepData, dtype = np.int16)
        write('TimbreAudio/%dHz_%dSec_OctSweep%dpartials_%s.wav' % (self.f_0, length, self.numPartials, self.harmonics ), 44100.0, sweepData)
        print "File written to TimbreAudio folder"



    def writeConsonantChord(self, verbose = False):  
        """
        Writes a chord with the selected half steps at the timbre's nearest consonant pitches. Prompts user for length and desired half steps.
        """
        self.audioGenPath()
        consRatios = [1] # initialize array
        self.consFreqs()
        consRatios[1:] = self.consonances/self.f_0
        EqTemp_Ratios = [(2**(1./12))**x for x in range(13)] # array of EQ Temp ratios, duh
        mins = []
        for i in range(len(consRatios)): # for each consonant frequency
            tmp = []
            for j in range(len(EqTemp_Ratios)): # for each 12TET step
                tmp.append(abs(consRatios[i] - EqTemp_Ratios[j])) # append tmp with the difference between ConsFreq and Step
            if tmp.index(min(tmp)) not in mins: # if the index isn't already in mins
                mins.append(tmp.index(min(tmp))) # add the min value for each i pass to the mins array
            else:
                mins.append(tmp.index(min(tmp))+1) # if it already is in mins, add one (i.e. make it the next half step up)
        # mins contains the indeces of the consFreqs, which corresponds to the interval, i.e. 3 is a minor 3rd, 7 is a 5th, etc
        ########
        while True:
            length = raw_input("Enter file length in seconds: ")
            try:
                length = (int(length))
                break
            except ValueError:
                print "Value must be an integer"

        chordNotes = []
        print "This timbre has %d consonances" % len(consRatios)
        while True:
            noteChoice = raw_input("Consonant half steps are %s. Enter the values you want; Press Enter twice when done: " % ', '.join([str(m) for m in mins]))
            try:
                noteChoiceInt = int(noteChoice) # will raise ValueError if noteChoice is '' or any string
                if noteChoiceInt not in mins:
                    raise InputError
                chordNotes.append(noteChoiceInt)
            except ValueError:
                if noteChoice != '': # noteChoice is not an int or ''
                    print "Value must be an integer"
                elif noteChoice == '' and not chordNotes:
                    print "Value must be an integer"
                else:
                    break
            except InputError:
                print "Value must be in list"
        ########
        sampleInc = 1.0/44100
        x = np.arange(0,length, sampleInc)
        wavData = np.zeros(len(x))
        noteDict = dict(zip(mins, consRatios))
        for freq,amp in zip(self.freqs,self.amps):
            for c in chordNotes:
                y = amp*np.sin(2*np.pi*noteDict[c]*freq*x)
                wavData = np.sum([wavData,y], axis = 0)
        mx = 1.1*(max(abs(wavData)))
        wavData = np.asarray(wavData)
        wavData = wavData/mx
        wavData = np.asarray(32000*wavData, dtype = np.int16)
        write('TimbreAudio/%dHzFund_%s_%sConsonantChord.wav' % (self.f_0, '-'.join([str(note) for note in sorted(chordNotes)]), self.harmonics), 44100.0, wavData)
        self.consonances = []
        print "File written to TimbreAudio folder"


    def writeEqTempChord(self): # , chordNotes = [0,4,7]
        """
        Writes an equal tempered chord with the selected half steps. Prompts user for length and desired half steps.
        """
        self.audioGenPath()
        EqTemp_Ratios = [(2**(1.0 / 12))**x for x in range(13)]
        while True:
            length = raw_input("Enter file length in seconds: ")
            try:
                length = (int(length))
                break
            except ValueError:
                print "Must be an integer"
        chordNotes = []
        while True:
            noteChoice = raw_input("Enter the half step values you want; Press Enter twice when done: ")
            try:
                chordNotes.append(int(noteChoice))
            except ValueError:
                if noteChoice != '':
                    print "Value must be an integer"
                elif noteChoice == '' and not chordNotes:
                    print "Value must be an integer"
                else:
                    break
        sampleInc = 1.0/44100
        x = np.arange(0,length, sampleInc)
        wavData = np.zeros(len(x))
        noteDict = dict(zip(range(0,len(EqTemp_Ratios)), EqTemp_Ratios))
        for freq,amp in zip(self.freqs,self.amps):
            for c in chordNotes:
                y = amp*np.sin(2 * np.pi * noteDict[c] * freq * x)
                wavData = np.sum([wavData,y], axis = 0)
        mx = 1.1*(max(abs(wavData)))
        wavData = np.asarray(wavData)
        wavData = wavData/mx
        wavData = np.asarray(32000*wavData, dtype = np.int16)
        write('TimbreAudio/%dHzFund_%s_%s_EqTemp_Chord.wav' % (self.f_0, '-'.join([str(note) for note in sorted(chordNotes)]), self.harmonics), 44100.0, wavData)
        print "File written to TimbreAudio folder"
        
        
    # def writeConsFreqs(self, length = 5):
    #     """Generates audio data and a .wav file of a timbre.
    #            * Default length 5 seconds.
    #            * files in TimbreAudio in cwd
    #     """
    #     self.audioGenPath()
    #     sampleInc = 1.0/44100
    #     consRatios = [1] # initialize array
    #     self.consFreqs()
    #     consRatios[1:] = self.consonances/self.f_0
    #
    #     EqTemp_Ratios = [(2**(1./12))**x for x in range(13)] # array of EQ Temp ratios, duh
    #
    #     print "This timbre has %d consonances" % len(consRatios)
    #
    #     mins = []
    #     for i in range(len(consRatios)): # for each consonant frequency
    #         tmp = []
    #         for j in range(len(EqTemp_Ratios)): # for each 12TET step
    #             tmp.append(abs(consRatios[i] - EqTemp_Ratios[j])) # append tmp with the difference between ConsFreq and Step
    #         if tmp.index(min(tmp)) not in mins: # if the index isn't already in mins
    #             mins.append(tmp.index(min(tmp))) # add the min value for each i pass to the mins array
    #             # print 'consRatios[%d] not moved' % i
    #         else:
    #             mins.append(tmp.index(min(tmp))+1) # if it already is in mins, add one (i.e. make it the next half step up)
    #     x = np.arange(0,length, sampleInc)
    #     wavData = np.zeros(len(x))
    #
    #     for i,(freq,amp) in enumerate(zip(self.freqs,self.amps)):
    #         y = amp*np.sin(2*np.pi*freq*x)
    #         wavData = np.sum([wavData,y], axis = 0)
    #
    #     mx = 1.1*(max(abs(wavData)))
    #     wavData = np.asarray(wavData)
    #     wavData = wavData/mx
    #     if hasattr(self, 'env'):
    #         wavData = self.env * wavData
    #     wavData = np.asarray(32000*wavData, dtype = np.int16)
    #     write('TimbreAudio/%dHz_%dpartials_%s.wav' % (self.f_0, self.numPartials, self.harmonics ), 44100.0, wavData)
    #     print "File written to TimbreAudio folder"
class Error(Exception):
    pass

class InputError(Error):
    pass
        

if __name__ == '__main__':
    from generators import *
    # # print os.path.dirname(os.path.realpath(__file__))
    # f = [260.44805563090279, 520.35237836904787, 778.62550242892019, 1039.6172909525806, 1300.609079476241, 1558.3384706433555, 1819.330259167016, 2078.6908490124033]
    # a = [0.16724917882935164, 1.0, 0.05825872786812774, 0.019126990466560075, 0.097543923859240947, 0.014853679015129385, 0.013322988640851378, 0.012819862560537666]
    # f,a = sfft.simple_fft('./samples/Bassoon.ff.C4.wav', mkPlot = True)
    # foo = Custom(f,a)
    # print 'len(f) = ', len(f)
    foo = Even()
    # # foo.timbreSweep(length = 60)
    # foo.disMeasure(octaves = 1)
    # # foo.timbreGen()
    
    # # foo.consDisFreqs()
    # foo.consFreqs(makePlot = True)
    foo.writeChord(length = 5, verbose = True)
    # # foo.partialsPlot()
    # foo.wavePlot()
    # foo.disPlot()
    # foo.disPlot(False)
    
    # f,a = fft6.get_fft_freq_array('./samples/Bassoon.ff.C4.wav', mkPlot = False, verbose = False)
    # print f
    # print a
    
    # bar = even(numPartials = 10)
    # bar.dismeasure(octaves = 2)
    # # bar.timbreGen()
    # #
    # baz = even(numPartials = 20)
    # baz.dismeasure(octaves = 2)
    # baz.timbreGen()
    # moo = sawtooth(numPartials = 7)
    # moo.dismeasure(octaves = 1)
    # moo.wavePlot()
    # moo.consDisFreqs()
    # moo.timbreGen()
    # disPlotMultiple(foo, bar, baz, moo)





