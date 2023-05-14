import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class NetSizeWindow:
    def __init__(self, win, master):
        self.master = master
        self.win = win
        self.win.grab_set()
        self.win.focus_set()
        self.win.title('Network setup')
        self.win.geometry("300x180")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the number of devices in the network:')
        self.lbl_init_network.place(x=20, y=20)
        
        self.inputtxt_n = tk.Text(self.win,
                   height = 1,
                   width = 32)
        self.inputtxt_n.place(x=20, y=50)
        self.inputtxt_n.bind('<Return>', self.return_key)

        self.lbl_init_network = tk.Label(win, text='Enter the network density:')
        self.lbl_init_network.place(x=20, y=80)
        
        self.density_value_label = tk.Label(
                        self.win,
                        text=f"{50}%")
        self.density_value_label.place(x=235, y=100)

        self.current_density = tk.DoubleVar()

        self.slider_density = ttk.Scale(
                        self.win,
                        from_=0,
                        length=210,
                        to=100,
                        orient='horizontal',
                        value=50,
                        variable= self.current_density,
                        command= lambda x: self.slider_changed(x, self.density_value_label))
        self.slider_density.set(50)
        self.slider_density.place(x=20, y=100)

        self.btn_enter = tk.Button(self.win,
                        text = "Enter", 
                        command = self.set_size)
        self.btn_enter.place(x=100, y=135)

        self.btn_cancel = tk.Button(self.win,
                        text = "Cancel", 
                        command = self.win.destroy)
        self.btn_cancel.place(x=150, y=135)

    def return_key(self, event):
        self.set_size()

    def slider_changed(self, value, label):
        label.configure(text='{: .2f}'.format(float(value))+'%')

    def set_size(self):
        n = self.inputtxt_n.get(1.0, "end-1c")
        if (n.isdigit() and int(n)>1):
            density = round(self.current_density.get()/100,2)
            self.master.create_network(net_size=int(n), density=density)
            self.win.destroy()
            self.master.init_params()
        elif (n.isdigit() and int(n)<=1):
            messagebox.showerror(message="The network must have at least 2 devices")
        else:
            messagebox.showerror(message="The network size must be an integer")