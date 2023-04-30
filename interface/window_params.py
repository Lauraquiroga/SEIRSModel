import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ModelParamsWindow:
    def __init__(self, win, master):
        self.master=master
        self.win = win
        self.win.title('Parameters')
        self.win.geometry("300x250")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the model parameters:')
        self.lbl_init_network.place(x=20, y=20)

        self.lbl_alpha = tk.Label(win, text='Alpha:')
        self.lbl_alpha.place(x=20, y=60)

        self.a_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.a_value_label.place(x=80, y=60)

        self.current_alpha = tk.DoubleVar()

        self.slider_a = ttk.Scale(
                        self.win,
                        from_=0,
                        length=150,
                        to=1,
                        orient='horizontal',
                        value=0.5,
                        variable= self.current_alpha,
                        command= lambda x: self.slider_changed(x, self.a_value_label))
        self.slider_a.set(0.5)
        self.slider_a.place(x=130, y=60)
        

        self.lbl_beta = tk.Label(win, text='Beta:')
        self.lbl_beta.place(x=20, y=90)
        
        self.b_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.b_value_label.place(x=80, y=90)

        self.current_beta = tk.DoubleVar()

        self.slider_b = ttk.Scale(
                        self.win,
                        length=150,
                        from_=0,
                        to=1,
                        orient='horizontal',
                        value=0.5,
                        variable= self.current_beta,
                        command= lambda x: self.slider_changed(x, self.b_value_label))
        self.slider_b.set(0.5)
        self.slider_b.place(x=130, y=90)

        self.lbl_delta = tk.Label(win, text='Delta:')
        self.lbl_delta.place(x=20, y=120)
        self.d_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.d_value_label.place(x=80, y=120)

        self.current_delta = tk.DoubleVar()

        self.slider_d = ttk.Scale(
                        self.win,
                        length=150,
                        from_=0,
                        to=1,
                        orient='horizontal',
                        value=0.5,
                        variable= self.current_delta,
                        command= lambda x: self.slider_changed(x, self.d_value_label))
        
        self.slider_d.set(0.5)
        self.slider_d.place(x=130, y=120)

        self.lbl_gamma = tk.Label(win, text='Gamma:')
        self.lbl_gamma.place(x=20, y=150)
        self.g_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.g_value_label.place(x=80, y=150)

        self.current_gamma = tk.DoubleVar()

        self.slider_g = ttk.Scale(
                        self.win,
                        length=150,
                        from_=0,
                        to=1,
                        orient='horizontal',
                        value=0.5,
                        variable= self.current_gamma,
                        command= lambda x: self.slider_changed(x, self.g_value_label))
        
        self.slider_g.set(0.5)
        self.slider_g.place(x=130, y=150)
        

        self.btn_enter = tk.Button(self.win,
                        text = "Enter", 
                        command = self.set_params)
        self.btn_enter.place(x=100, y=200)

        self.btn_cancel = tk.Button(self.win,
                        text = "Cancel", 
                        command = self.win.destroy)
        self.btn_cancel.place(x=150, y=200)


    def set_params(self):
        alpha = round(self.current_alpha.get(),2)
        beta = round(self.current_beta.get(),2)
        delta = round(self.current_delta.get(),2)
        gamma = round(self.current_gamma.get(),2)

        self.master.run_model(alpha, beta, delta, gamma)
        self.win.destroy()
                
    def slider_changed(self, value, label):
        label.configure(text='{: .2f}'.format(float(value)))