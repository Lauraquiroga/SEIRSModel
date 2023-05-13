import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class NetSizeWindow:
    def __init__(self, win, master):
        self.master = master
        self.win = win
        self.win.title('Network setup')
        self.win.geometry("300x170")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the number of devices in the network:')
        self.lbl_init_network.place(x=20, y=20)
        
        self.inputtxt_n = tk.Text(self.win,
                   height = 1,
                   width = 32)
        self.inputtxt_n.place(x=20, y=50)
        self.inputtxt_n.bind('<Return>', self.return_key)

        self.lbl_init_network = tk.Label(win, text='Enter the network density:')
        self.lbl_init_network.place(x=20, y=70)
        
        self.density_value_label = tk.Label(
                        self.win,
                        text=50)
        self.density_value_label.place(x=230, y=90)

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
        self.slider_density.place(x=20, y=90)

        self.btn_enter = tk.Button(self.win,
                        text = "Enter", 
                        command = self.set_size)
        self.btn_enter.place(x=100, y=120)

        self.btn_cancel = tk.Button(self.win,
                        text = "Cancel", 
                        command = self.win.destroy)
        self.btn_cancel.place(x=150, y=120)

    def return_key(self, event):
        self.set_size()

    def slider_changed(self, value, label):
        label.configure(text='{: .2f}'.format(float(value)))

    def set_size(self):
        n = self.inputtxt_n.get(1.0, "end-1c")
        if (n.isdigit()):
            density = round(self.current_density.get(),2)
            print(density)
            self.master.create_network(net_size=int(n))
            self.win.destroy()
            self.master.init_params()
        else:
            messagebox.showerror(message="The netwrok size must be an integer")