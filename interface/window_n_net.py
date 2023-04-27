import tkinter as tk
from tkinter import messagebox

class NetSizeWindow:
    def __init__(self, win, master):
        self.master = master
        self.win = win
        self.win.title('Network size')
        self.win.geometry("300x150")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the number of devices in the network:')
        self.lbl_init_network.place(x=20, y=20)
        
        self.inputtxt_n = tk.Text(self.win,
                   height = 1,
                   width = 32)
        self.inputtxt_n.place(x=20, y=50)

        self.btn_enter = tk.Button(self.win,
                        text = "Enter", 
                        command = self.set_size)
        self.btn_enter.place(x=100, y=80)

        self.btn_cancel = tk.Button(self.win,
                        text = "Cancel", 
                        command = self.win.destroy)
        self.btn_cancel.place(x=150, y=80)


    def set_size(self):
        n = self.inputtxt_n.get(1.0, "end-1c")
        if (n.isdigit()):
            self.master.create_network(net_size=int(n))
            self.win.destroy()
            self.master.init_params()
        else:
            messagebox.showerror(message="The netwrok size must be an integer")