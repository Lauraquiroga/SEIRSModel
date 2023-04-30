import tkinter as tk

class InitInfectionWindow:
    def __init__(self, win, master):
        self.master=master
        self.win = win
        self.win.title('Initially infected')
        self.win.geometry("500x500")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Choose initially infected device:')
        self.lbl_init_network.place(x=20, y=20)
