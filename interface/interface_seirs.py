import tkinter as tk
from tkinter import messagebox
from window_file_name import FileNameWindow
from window_n_net import NetSizeWindow
from window_params import ModelParamsWindow
from window_results import ResultsWindow
from model.network import Network
from model.seirs_model import SEIRS_Model

class InterfaceSEIRS:
    def __init__(self, win):
        self.win = win

        self.lbl_init_network = tk.Label(win, text='Select how to initialize the network:')
        self.lbl_init_network.place(x=20, y=20)

        self.load_mode = tk.IntVar()
        self.load_mode.set(1)
        self.rdbtn_load_prob = tk.Radiobutton(win, text='Load network with initial probabilities from file', variable=self.load_mode, value=1)
        self.rdbtn_load_noprob = tk.Radiobutton(win, text='Load network structure from file (no initial probabilities)', variable=self.load_mode, value=2)
        self.rdbtn_generate_new = tk.Radiobutton(win, text='Generate new random network', variable=self.load_mode, value=3)
        self.rdbtn_load_prob.place(x=20, y=50)
        self.rdbtn_load_noprob.place(x=20, y=70)
        self.rdbtn_generate_new.place(x=20, y=90)

        self.btn_start = tk.Button(text='Initialize network', command=self.init_network, bg='black', fg='white')
        self.btn_start.place(x=130, y=140)

    def init_network(self):
        child_win = tk.Toplevel(self.win)

        if self.load_mode.get()!=3:
            FileNameWindow(child_win, self)
            self.win.mainloop

        else:
            NetSizeWindow(child_win, self)
            self.win.mainloop
        
    def create_network(self, file_name="", net_size=0):
        if self.load_mode.get()!=3:
            try:
                self.network = Network(self.load_mode.get(), file_name=file_name)
            except FileNotFoundError as e:
                mess = str(e).split('] ', 1)[1]
                messagebox.showerror(message=mess)
        else:
            self.network = Network(self.load_mode.get(), net_size=net_size)
    
    def init_params(self):
        child_win = tk.Toplevel(self.win)
        ModelParamsWindow(child_win, self)
        self.win.mainloop

    def run_model(self, alpha, beta, delta, gamma):
        #rates:= dictionary with parameters
        rates = {'alpha': alpha, 'beta':beta, 'delta':delta, 'gamma':gamma}
        #initialize and run the model
        model = SEIRS_Model(self.network, 1000, rates)
        model.run_model()
        self.show_results(model)

    def show_results(self, model):
        child_win = tk.Toplevel(self.win)
        ResultsWindow(child_win, self, model)
        self.win.mainloop

def main(): 
    root = tk.Tk()
    root.title("SEIRS Model")
    root.geometry("370x200")
    root.resizable(0,0)
    InterfaceSEIRS(root)
    root.mainloop()

if __name__ == '__main__':
    main()