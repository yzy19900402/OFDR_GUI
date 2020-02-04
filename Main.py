import Gui
import math

#global paramters
TARGET_IP = ''
TARGET_PORT = 8001
Data_length = 65536# the data length for u64, 8bytes
UDP_MAX = 32768  # the max byte length for UDP
COLUMN_NUM = math.floor(UDP_MAX / 8)
folder = '/home/clark/Documents/Measurements/01_15_20_Fiber_cable_ID/226ns/01_23_20_Cables/CableAA1/'
folder_number = 1


gui = Gui.gui_window(folder, Data_length, folder_number, UDP_MAX, COLUMN_NUM, TARGET_IP, TARGET_PORT)

gui.Start_gui()