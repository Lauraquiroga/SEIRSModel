import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class ModelParamsWindow:
    def __init__(self, win, master):
        self.master=master
        self.win = win
        self.win.title('Parameters')
        self.win.geometry("500x250")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the model parameters:')
        self.lbl_init_network.place(x=20, y=20)

        self.lbl_alpha = tk.Label(win, text=chr(945))
        self.lbl_alpha.place(x=20, y=90)

        self.a_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.a_value_label.place(x=60, y=90)

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
        self.slider_a.place(x=100, y=90)
        

        self.lbl_beta = tk.Label(win, text=chr(946))
        self.lbl_beta.place(x=20, y=60)
        
        self.b_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.b_value_label.place(x=60, y=60)

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
        self.slider_b.place(x=100, y=60)

        self.lbl_delta = tk.Label(win, text=chr(948))
        self.lbl_delta.place(x=20, y=120)
        self.d_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.d_value_label.place(x=60, y=120)

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
        self.slider_d.place(x=100, y=120)

        self.lbl_gamma = tk.Label(win, text=chr(947))
        self.lbl_gamma.place(x=20, y=150)
        self.g_value_label = tk.Label(
                        self.win,
                        text=0.5)
        self.g_value_label.place(x=60, y=150)

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
        self.slider_g.place(x=100, y=150)
        

        self.btn_enter = tk.Button(self.win,
                        text = "See Equations", 
                        command = self.see_equations)
        self.btn_enter.place(x=30, y=200)

        self.btn_enter = tk.Button(self.win,
                        text = "Enter", 
                        command = self.set_params)
        self.btn_enter.place(x=130, y=200)

        self.btn_cancel = tk.Button(self.win,
                        text = "Cancel", 
                        command = self.win.destroy)
        self.btn_cancel.place(x=180, y=200)

        # Display diagram
        self.diagram = self.load_image("seirsDiagram.png", (200,200))
        self.label = tk.Label(self.win,image=self.diagram)
        self.label.place(x=280, y=20)

        self.equationsDisplayed = False


    def set_params(self):
        """
        Set model parameter (rates) values
        """
        alpha = round(self.current_alpha.get(),2)
        beta = round(self.current_beta.get(),2)
        delta = round(self.current_delta.get(),2)
        gamma = round(self.current_gamma.get(),2)

        if self.master.load_mode.get()==1:
            self.master.run_model(alpha, beta, delta, gamma)
        else:
            self.master.set_initially_inf(rates=[alpha, beta, delta, gamma])

        self.win.destroy()
    
    def see_equations(self):
        """
        Display model equations in a new window
        """
        if not self.equationsDisplayed:
            self.child_win = tk.Toplevel(self.win)
            self.child_win.title("Model equations")
            self.child_win.geometry("320x320")
            self.child_win.resizable(0,0)

            self.eqs=self.load_image("equations.png", (300, 300))
            self.eqlabel = tk.Label(self.child_win,image=self.eqs)
            self.eqlabel.pack()
            self.equationsDisplayed=True

            # Bind kill root to destroy event with close button
            self.child_win.protocol("WM_DELETE_WINDOW", self.not_displayed)

        else:
            self.child_win.lift()

    def not_displayed (self):
        self.equationsDisplayed=False
        self.child_win.destroy()
                
    def slider_changed(self, value, label):
        label.configure(text='{: .2f}'.format(float(value)))

    def load_image(self, name, size):
        """
        Load and resize image from assets
        """
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, 'assets', f"{name}")
        image = Image.open(image_path)
        return ImageTk.PhotoImage(image.resize(size))
