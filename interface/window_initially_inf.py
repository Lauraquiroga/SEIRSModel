import tkinter as tk
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model.network import Network

class InitInfectionWindow:
    def __init__(self, win, master, rates):
        self.master=master
        self.win = win
        self.win.grab_set()
        self.win.focus_set()
        self.win.title('Initial conditions')
        self.win.geometry("1000x700")
        self.win.resizable(0,0)
        self.network:Network = self.master.network
        self.rates = rates

        self.lbl_init_network = tk.Label(win, text='To run the model varying the\ninitially infected device, choose\nnumber of time-steps to consider:',
                                         justify='left')
        self.lbl_init_network.place(x=15, y=70)

        iterations = [x for x in range(1,31)]
        self.cb_its=Combobox(win, values=iterations, state="readonly", width=10)
        self.cb_its.current(14)
        self.cb_its.place(x=20, y=130)

        self.btn_choose = tk.Button(master=self.win, text='Go!', command=self.run_heat_map)
        self.btn_choose.place(x=120, y=127)

        self.lbl_init_network = tk.Label(win, text='Otherwise\nselect initially infected node:', justify="left")
        self.lbl_init_network.place(x=15, y=250)

        nodes = [x for x in range(self.network.n)]
        self.cb_nodes=Combobox(win, values=nodes, state="readonly", width=10)
        self.cb_nodes.current(0)
        self.cb_nodes.place(x=20, y=310)

        self.btn_choose = tk.Button(master=self.win, text='Select', command=self.choose_node)
        self.btn_choose.place(x=120, y=307)

        # Display graph
        self.show_graph()

    def show_graph(self):
        self.fig = self.network.draw_graph_structure()
        canvas = FigureCanvasTkAgg(self.fig, master = self.win)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.win)
        toolbar.update()
        toolbar.place(x=600, y=20)
        canvas.get_tk_widget().place(x=200, y=70)

    def choose_node(self):
        init_inf = int(self.cb_nodes.get())
        self.network.initialize_probs(init_inf)
        self.master.run_model(self.rates[0],
                              self.rates[1],
                              self.rates[2],
                              self.rates[3],
                              False)
        self.win.destroy()

    def run_heat_map(self):
        n_times = int(self.cb_its.get())
        self.master.run_model(self.rates[0],
                              self.rates[1],
                              self.rates[2],
                              self.rates[3],
                              True, n_times)
        self.win.destroy()