import scipy
import numpy as np
from scipy.io import wavfile

SUBTRACTION_FACTOR = 1.5 
OVERSUBTRACTION = 0.5
MUSICAL_NOISE_LEVEL = 0.1


class Noiseremover():
    def __init__(self, rate):
        self.windowlen = 0.032
        self.framelength = rate * self.windowlen  # to make frames equal to 256 for fast fft in 8khz signal
        self.noiseprofile = np.zeros(self.framelength)  # storage for silence spectrums additions


    def buildnoiseprofile(self, data, nosecs=0.8):
        ''' noframes: no of frames to average '''
        noframes = np.floor(nosecs / self.windowlen)

        for i in range(int(noframes)):
            start = i * (self.framelength / 2)  # for overlapping 50% of frames
            ftd = scipy.fft(data[start: start + self.framelength] * np.hamming(self.framelength))
            mag = np.abs(ftd)
            self.noiseprofile += mag

        self.noiseprofile = self.noiseprofile / noframes  # averaging the totals

    def removenoise(self, data):
        nototalframes = np.floor(len(data) / (self.framelength)) - 1  # the total no of frames in sound
        dataclean = np.array([])  # storage for final sound

        # record short brusts storage for musical short lived noise
        f1 = np.array(256)
        f1a = np.array(256)
        f1b = np.zeros(256)
        f2 = np.array(256)
        f2a = np.array(256)
        f2b = np.zeros(256)
        f3 = np.array(256)
        f3a = np.array(256)
        f3b = np.zeros(256)
        f4 = np.array(256)
        f4a = np.array(256)
        f4b = np.zeros(256)


        for i in range(int(nototalframes)):
            start = i * (self.framelength)
            dft = scipy.fft(data[start: start + self.framelength])  # no windowing .. required?
            dmag = np.abs(dft)
            dang = np.angle(dft)
            dmag = dmag - SUBTRACTION_FACTOR * self.noiseprofile # subtract the noise spectrum by 1.5 for greater effect
            dmag[36:220] = dmag[36 :220] - OVERSUBTRACTION * self.noiseprofile[36: 220]  #over subtraction    above 2kh
            dmag[dmag < 0] = 0  # because magnitude spectrum cannot be -ve


            #remove musical noise7
            dnos = (dmag < MUSICAL_NOISE_LEVEL) & (dmag >0)

            if i>3:
                delindex = np.logical_and.reduce((f1b, f2b, f3b, f4b,np.logical_not(dnos)))
                f1[delindex] =0
                f2[delindex] = 0
                f2b[delindex] =0
                f3[delindex] = 0
                f3b[delindex] = 0
                f4[delindex] = 0
                f4b[delindex] =0

                delindex = np.logical_and.reduce((f2b, f3b, f4b,np.logical_not(dnos)))
                f2[delindex] = 0
                f2b[delindex] =0
                f3[delindex] = 0
                f3b[delindex] = 0
                f4[delindex] = 0
                f4b[delindex] =0

                delindex = np.logical_and.reduce((f3b, f4b,np.logical_not(dnos)))
                f3[delindex] = 0
                f3b[delindex] =0
                f4[delindex] = 0
                f4b[delindex] = 0

                delindex = np.logical_and(f4b, np.logical_not(dnos))
                f4[delindex] = 0
                f4b[delindex] = 0

                #revert to time domain
                new = f1 * np.exp(f1a * 1j)  # integrate new magnitude and old phase mag*e^(j*phase)
                idft = scipy.ifft(new)  # time domain
                dataclean = np.append(dataclean, np.real(idft))

            ##swap values
            f1=f2
            f1a=f2a
            f1b= f2b
            f2=f3
            f2a=f3a
            f2b=f3b
            f3= f4
            f3a = f4a
            f3b =f4b
            f4= dmag
            f4a = dang
            f4b = dnos

        new = f2 * np.exp(f2a * 1j)  # integrate new magnitude and old phase mag*e^(j*phase)
        idft = scipy.ifft(new)  # time domain
        dataclean = np.append(dataclean, np.real(idft))
        new = f3 * np.exp(f3a * 1j)  # integrate new magnitude and old phase mag*e^(j*phase)
        idft = scipy.ifft(new)  # time domain
        dataclean = np.append(dataclean, np.real(idft))
        new = f4 * np.exp(f4a * 1j)  # integrate new magnitude and old phase mag*e^(j*phase)
        idft = scipy.ifft(new)  # time domain
        dataclean = np.append(dataclean, np.real(idft))
        new = dmag * np.exp(dang * 1j)  # integrate new magnitude and old phase mag*e^(j*phase)
        idft = scipy.ifft(new)  # time domain
        dataclean = np.append(dataclean, np.real(idft))
        return dataclean


if __name__ == '__main__':
    rate, data = wavfile.read('recorded.wav')

    data = data / (2. ** 15)  # convert quantised values into real value for 16bit audio

    noiser = Noiseremover(rate)
    noiser.buildnoiseprofile(data, nosecs=0.8)
    cleandata = noiser.removenoise(data)

    cleandata = cleandata * (2. ** 15)
    cleandata= np.array(cleandata, np.int16)

    wavfile.write('avassilenceremove.wav', rate, cleandata)
