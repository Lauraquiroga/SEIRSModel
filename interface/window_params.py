import tkinter as tk
from tkinter import messagebox

class ModelParamsWindow:
    def __init__(self, win, master):
        self.master=master
        self.win = win
        self.win.title('Model parameters')
        self.win.geometry("220x220")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the model parameters:')
        self.lbl_init_network.place(x=20, y=20)

        self.lbl_alpha = tk.Label(win, text='Alpha:')
        self.lbl_alpha.place(x=20, y=60)
        self.inputtxt_a = tk.Text(self.win,
                   height = 1,
                   width = 10)
        self.inputtxt_a.place(x=80, y=60)

        self.lbl_beta = tk.Label(win, text='Beta:')
        self.lbl_beta.place(x=20, y=80)
        self.inputtxt_b = tk.Text(self.win,
                   height = 1,
                   width = 10)
        self.inputtxt_b.place(x=80, y=80)

        self.lbl_delta = tk.Label(win, text='Delta:')
        self.lbl_delta.place(x=20, y=100)
        self.inputtxt_d = tk.Text(self.win,
                   height = 1,
                   width = 10)
        self.inputtxt_d.place(x=80, y=100)

        self.lbl_gamma = tk.Label(win, text='Gamma:')
        self.lbl_gamma.place(x=20, y=120)
        self.inputtxt_g = tk.Text(self.win,
                   height = 1,
                   width = 10)
        self.inputtxt_g.place(x=80, y=120)
        

        self.btn_enter = tk.Button(self.win,
                        text = "Enter", 
                        command = self.set_params)
        self.btn_enter.place(x=60, y=165)

        self.btn_cancel = tk.Button(self.win,
                        text = "Cancel", 
                        command = self.win.destroy)
        self.btn_cancel.place(x=110, y=165)


    def set_params(self):
        alpha = self.inputtxt_a.get(1.0, "end-1c")
        beta = self.inputtxt_b.get(1.0, "end-1c")
        delta = self.inputtxt_d.get(1.0, "end-1c")
        gamma = self.inputtxt_g.get(1.0, "end-1c")
        try:
                alpha = float(alpha)
                beta = float(beta)
                delta = float(delta)
                gamma = float(gamma)

                self.master.run_model(alpha, beta, delta, gamma)
                self.win.destroy()
                
        except ValueError:
            messagebox.showerror(message="The model parameters must be a numeric type")