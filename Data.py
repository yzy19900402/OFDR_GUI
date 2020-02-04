import numpy as np
import socket
import math
import Gui


# folder = './data/'

# Socket part capture the data

class Data:
    Data_length = 0
    UDP_MAX = 1
    TARGET_IP = ''
    TARGET_PORT = 8001
    TARGET = (TARGET_IP, TARGET_PORT)
    COLUMN_NUM = 0
    ADC_data_A = 0
    ADC_data_B = 0
    DAC_data = 0
    CMP_Delay = 0
    Dn = 0
    CMP_in = 0
    Trigger = 0
    Up = 0
    Phase_error = 0
    folder_number = 0
    folder = 0
    ss = 0
    Depth = 1
    data_ready = False
    i = 0
    data = 0

    def __init__(self, folder, Data_length, folder_number, UDP_MAX, COLUMN_NUM, TARGET_IP, TARGET_PORT):
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.TARGET = (TARGET_IP, TARGET_PORT)
        self.ss.bind(self.TARGET)
        self.folder = folder
        self.folder_number = folder_number
        self.ADC_data_A = np.zeros(Data_length, dtype=np.int16)
        self.ADC_data_B = np.zeros(Data_length, dtype=np.int16)
        self.DAC_data = np.zeros(Data_length, dtype=np.uint16)
        self.Other = np.zeros(COLUMN_NUM, dtype=np.uint16)
        self.Trigger = np.zeros(Data_length, dtype=np.uint8)
        self.Up = np.zeros(Data_length, dtype=np.uint8)
        self.Dn = np.zeros(Data_length, dtype=np.uint8)
        self.CMP_in = np.zeros(Data_length, dtype=np.uint8)
        self.CMP_Delay = np.zeros(Data_length, dtype=np.uint8)
        self.Phase_error = np.zeros(Data_length, dtype=np.int16)
        self.data_ready = False
        self.temp_buffer = np.zeros([math.floor(Data_length * 8 / UDP_MAX), UDP_MAX], dtype=np.uint8)
        self.Data_length = Data_length
        self.UDP_MAX = UDP_MAX
        self.Depth = math.floor(self.Data_length*8/self.UDP_MAX)

    def close(self):
        self.stop_thread = True

    def reset(self):
        self.i = self.Depth - 1

    def Try_data_run(self):
        self.ss.settimeout(0.05)
        try:
            data, addrRsv = self.ss.recvfrom(self.UDP_MAX)
        except:
            return False
        else:
            # print(self.i)
            if not self.data_ready:
                if data[7] == 0x5a:
                    self.i = 0

            if data[7] == 0xa5:
                if self.i == self.Depth - 1:
                    self.data_ready = True
                    # print('Ready')

            self.temp_buffer[self.i, :] = np.frombuffer(data, dtype=np.uint8)
            self.i = (self.i + 1) % self.Depth
            if self.data_ready:
                self.data_ready = False
                data = self.temp_buffer.tobytes()
                self.data = np.frombuffer(data, np.int16)
                data_temp = np.reshape(self.data, [self.Data_length, 4])
                self.ADC_data_A = data_temp[:, 0]
                self.ADC_data_B = data_temp[:, 1]
                DAC_data_temp = data_temp[:, 2]
                self.DAC_data = DAC_data_temp.astype(np.uint16)
                Other = data_temp[:, 3]
                Other = Other.astype(np.uint16)
                self.CMP_Delay = Other % 2
                self.Dn = ((Other // 2) % 16)
                self.CMP_in = (Other // pow(2, 5)) % 2
                self.Trigger = (Other // pow(2, 6)) % 2
                self.Up = (Other // pow(2, 7)) % 2
                Upcumsum = self.Up.cumsum()
                Dncumsum = self.Dn.cumsum()
                self.data_ready = False
                self.Phase_error = np.int16(Upcumsum - Dncumsum)
                return True
            else:
                return False
            # print(self.i)
            # Debug_test = self.DAC_data
            # print(Debug_test)
            # break

    def save_data(self, name):
        print('Saving')
        np.savetxt(name + '/MZI.txt', self.ADC_data_A)
        np.savetxt(name + '/Reflect.txt', self.ADC_data_B)
        np.savetxt(name + '/Up.txt', self.Up)
        np.savetxt(name + '/Dn.txt', self.Dn)
        np.savetxt(name + '/CMP_Delay.txt', self.CMP_Delay)
        np.savetxt(name + '/CMP_in.txt', self.CMP_in)
        np.savetxt(name + '/DAC.txt', self.DAC_data)
        np.savetxt(name + '/Trigger.txt', self.Trigger)
        return 'Saved'

    def get_shot(self):
        return self.DAC_data

    def if_ready(self):
        return self.data_ready

    def get_data(self):
        return (self.ADC_data_A - np.mean(self.ADC_data_A)), (
                self.ADC_data_B - np.mean(
            self.ADC_data_B)), self.DAC_data, self.CMP_Delay, self.Trigger, self.CMP_in, self.Phase_error, self.Up, self.Dn
