import Data as DT
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

name = 'temp'
flag = False
lflag = False
ymax = 0
fs = 125e6
stop_thread = False
fp = 5
tau_d = 226e-9  # 1025e-9  # 226e-9
vp = 2e8  # The light speed in fiber
f0 = 43e3  # corresponding with L0


class DRAW:
    def __init__(self, DT):
        self.data_src = DT
        self.fig = plt.figure(figsize=(3, 2), dpi=100)
        self.fig.set_tight_layout(True)
        self.i = 0

    def Test(self):
        self.fig.clf()
        self.i += 5
        fig1 = plt.subplot(111)
        t = np.arange(1024)
        t = t*np.pi/512
        y = np.sin(t+self.i)
        plt.plot(t, y)
        plt.xlim(0, 6)
        plt.ylim(-1, 1)
        plt.grid()
        # SMALL_SIZE = 4
        # MEDIUM_SIZE = 10
        # BIGGER_SIZE = 12
        # plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
        # plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
        # plt.rc('axes', labelsize=SMALL_SIZE)  # fontsize of the x and y labels
        # plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        # plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        # plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
        # plt.rc('figure', titlesize=SMALL_SIZE)  # fontsize of the figure title
        # fig1.plot.grid()

    def Test_stop(self):
        self.fig.clf()

    def Work_moniter(self):
        print('started\n')
        self.fig.clf()
        index = np.arange(0, self.data_src.Data_length)
        t_us = index / fs * 1e6
        ADC_data_A, ADC_data_B, DAC_data, CMP_Delay, Trigger, COMP_in, Phase_error, Up, Dn = self.data_src.get_data()

        fig1 = plt.subplot(231)
        plt.plot(t_us, DAC_data / 39.7727, linewidth=0.8)
        plt.xlim(0, max(t_us))
        plt.grid()
        plt.xlabel('Time(\u03BCs)')
        plt.ylabel('Current(mA)')
        plt.title('Driving Current')

        fig2 = plt.subplot(232)
        plt.plot(t_us, ADC_data_A * 1000 / pow(2, 13), linewidth=0.8)
        plt.grid()
        plt.xlim(0, max(t_us))
        plt.xlabel('Time(\u03BCs)')
        plt.ylabel('Voltage (mV)')
        plt.title('MZI time domain signal')

        fig3 = plt.subplot(233)
        plt.plot(t_us, (Phase_error) / fp, linewidth=0.8)
        plt.grid()
        plt.xlim(0, max(t_us))
        plt.xlabel('Time(\u03BCs)')
        plt.ylabel('Phase error(\u03C0)')
        plt.title('Phase error over Time')

        f, t, Zxx = signal.stft(ADC_data_A, fs, nperseg=1000, noverlap=990)
        fig4 = plt.subplot(234)
        plt.pcolormesh(t * 1e6, f / 1e6, np.abs(Zxx))
        plt.ylabel('Frequency(MHz)')
        plt.xlabel('Time(\u03BCs)')
        plt.title('MZI STFFT')
        plt.xlim(0, max(t_us))
        plt.grid()
        plt.ylim(0, 30)

        fig5 = plt.subplot(2, 3, 5)
        freq = np.arange(int(self.data_src.Data_length))
        freq = freq * fs / self.data_src.Data_length
        sp = np.abs(np.fft.fft(ADC_data_A)) / self.data_src.Data_length
        # print(np.max(sp))
        sp_dB = 20 * np.log10(sp)
        plt.plot(freq / 1e6, sp_dB)
        plt.title('MZI FFT')
        plt.xlabel('Frequency(MHz)')
        plt.ylabel('magnitude(real dB)')
        plt.xlim(0, 30)
        # plt.ylim(max(sp_dB) - 40, max(sp_dB))
        plt.grid()

        fig6 = plt.subplot(2, 3, 6)
        sp = np.abs(np.fft.fft(ADC_data_B)) / self.data_src.Data_length
        # print(np.max(sp))
        sp_dB = 20 * np.log10(sp)
        distance = (freq - f0) / fs * tau_d * fp * vp
        plt.plot(distance, sp_dB)
        plt.title('Fiber length')
        plt.xlabel('Fiber length(m)')
        plt.ylabel('magnitude(real dB)')
        plt.xlim(-0.1, 6)
        # plt.ylim(max(sp_dB) - 70, max(sp_dB))
        plt.grid()


