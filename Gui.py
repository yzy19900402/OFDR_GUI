from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import Data as DT
import Draw
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import shlex
import subprocess
import os

class gui_window:
    #  The parameters
    color_bg = 'white'  # Set background color
    color_text = '#E1F5FE'  # Set text color
    color_btn = '#212121'  # Set button color
    color_line = '#01579B'  # Set line color
    color_can = '#212121'  # Set canvas colorcd ..
    color_oval = '#2196F3'  # Set oval color
    target_color = '#FF6D00'

    Debug_STOP = FALSE
    Work_STOP = FALSE
    Data_Save_STOP = TRUE
    i = 1

    def __init__(self, folder, Data_length, folder_number, UDP_MAX, COLUMN_NUM, TARGET_IP, TARGET_PORT):
        self.root = Tk()  # create root window
        self.root.title("OFDR Client")
        self.root.maxsize(800, 600)
        self.root.config(bg="skyblue")

        self.Data = DT.Data(folder, Data_length, folder_number, UDP_MAX, COLUMN_NUM, TARGET_IP, TARGET_PORT)

        # Create left and right frames
        self.Control_Frame = Frame(self.root, width=2560, height=200, bg='grey')
        self.Control_Frame.pack(side='bottom', fill='x', padx=10, pady=5, expand=False)

        self.Fig_Frame = Frame(self.root, width=2560, height=1200, bg='grey')
        self.Fig_Frame.pack(side='bottom', fill='both', padx=10, pady=5, expand=True)

        # self.tool_bar = Frame(self.Control_Frame, width=90, height=185, bg='lightgrey')
        # self.tool_bar.grid(side='left', fill='both', padx=5, pady=5, expand=True)

        self.Control_bar = Frame(self.Control_Frame, width=1024, height=200, bg='lightgrey')
        self.Control_bar.pack(side='left', fill='y', padx=10, pady=5, expand=False)

        self.Terminal_bar = Frame(self.Control_Frame, width=1536, height=200, bg='black')
        self.Terminal_bar.pack(side='left', fill='both', padx=10, pady=5, expand=True)

        wid = self.Terminal_bar.winfo_id()
        args = shlex.split('xterm -into %d -geometry 80x80 -sb -e command &' % (wid))
        # os.system('xterm -into %d -geometry 40x20 -sb -e command &' % wid)
        self.terminal = subprocess.Popen(args)
        self.root.protocol('WM_DELETE_WINDOW', self.before_close)

        # Example labels that serve as placeholders for other widgets
        Label(self.Control_bar, text="Control", font=64).grid(column=5, row=0, sticky='news')

        # For now, when the buttons are clicked, they only call the clicked() method. We will add functionality later.
        Button(self.Control_bar, text="Debug", command=self.ReDebug).grid(column=0, row=1, sticky='news')
        Button(self.Control_bar, text="Stop", command=self.Stop).grid(column=0, row=2, sticky='news')
        Button(self.Control_bar, text="Work", command=self.Restart).grid(column=0, row=3, sticky='news')

        self.E1 = tk.Entry(self.Control_bar, show=None, width=30, bg="#37474F", fg='#eceff1')
        self.E1.grid(column=2, row=1, columnspan=6, sticky='news')  #Define a Entry and put it in position
        self.E1.insert(0, './Debug')
        Button(self.Control_bar, text="Debug Save", command=self.Debug_Save_data).grid(column=10, row=1, sticky='news')

        self.E2 = tk.Entry(self.Control_bar, show=None, width=30, bg="#37474F", fg='#eceff1')
        self.E2.grid(column=2, row=2, columnspan=6, sticky='news')  #Define a Entry and put it in position
        self.E2.insert(0, '128')

        self.E3 = tk.Entry(self.Control_bar, show=None, width=30, bg="#37474F", fg='#eceff1')
        self.E3.grid(column=2, row=3, columnspan=6, sticky='news')  #Define a Entry and put it in position
        self.E3.insert(0, './Data')
        Button(self.Control_bar, text="Stream Save", command=self.Save_data_Stream).grid(column=10, row=3, sticky='news')

        self.Fig = Draw.DRAW(self.Data)
        self.canvas = FigureCanvasTkAgg(self.Fig.fig, master=self.Fig_Frame)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side='right', fill='both', padx=5, pady=5, expand=True)
        self.Fig.Test()
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, self.Fig_Frame)
        toolbar.config(background=self.color_bg)
        toolbar._message_label.config(background=self.color_bg)
        for button in toolbar.winfo_children():
            button.config(background=self.color_bg)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=0, pady=0)
        self.i = 1

    def ReDebug(self):
        self.Work_STOP = TRUE
        self.Data_Save_STOP = TRUE
        self.Debug_STOP = FALSE
        self.Debug()

    def Restart(self):
        self.Work_STOP = FALSE
        self.Debug_STOP = TRUE
        self.Data_Save_STOP = FALSE
        self.Work()

    def Stop(self):
        # print("tick")
        self.Work_STOP = TRUE
        self.Debug_STOP = TRUE
        self.Data_Save_STOP = FALSE

    def Start_gui(self):
        self.root.after(100, self.clicked)
        self.root.mainloop()

    def clicked(self):
        '''if button is clicked, display message'''
        print("Clicked.")

    def Debug_Save_data(self):
        name = self.E1.get()
        Status = self.Data.save_data(name)
        tk.messagebox.showinfo('Info', 'Debug data saved')

    def Save_data_Stream(self):
        self.Debug_STOP = TRUE
        self.Work_STOP = TRUE
        if self.Data_Save_STOP:
            self.i = 1
            print("Data saving stops")
        else:
            self.root.after(20, self.Save_data_Stream)
            if self.i < int(self.E2.get()):
                if self.Data.Try_data_run():
                    self.Fig.Work_moniter()
                    self.canvas.draw()
                    name = self.E3.get() + '/' + str(self.i) + '/'
                    print(name)
                    Status = self.Data.save_data(name)
                    self.i += 1
            else:
                self.Data_Save_STOP = TRUE
                tk.messagebox.showinfo('Info', 'Stream data saved')


    def Debug(self):
        if self.Debug_STOP:
            print("Debug stops")
        else:
            self.Fig.Test()
            self.canvas.draw()
            self.root.after(20, self.Debug)

    def Work(self):
        if self.Work_STOP:
            print("Working stops")
        else:
            self.root.after(20, self.Work)
            if self.Data.Try_data_run():
                self.Fig.Work_moniter()
                self.canvas.draw()

    def before_close(self):
        # self.terminal.terminate()
        self.root.destroy()

