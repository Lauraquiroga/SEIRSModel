import tkinter as tk
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model.network import Network

class InitInfectionWindow:
    def __init__(self, win, master, network:Network):
        self.master=master
        self.win = win
        self.win.title('Initially infected')
        self.win.geometry("500x500")
        self.win.resizable(0,0)
        self.network = network

        self.lbl_init_network = tk.Label(win, text='Choose initially infected device:')
        self.lbl_init_network.place(x=20, y=20)

        # Display graph
        self.show_graph()

        nodes = [x for x in range(self.results.n)]
        self.cb_nodes=Combobox(win, values=nodes, state="readonly", width=10)
        self.cb_nodes.current(0)
        self.cb_nodes.place(x=380, y=40)

    def show_graph(self):
        self.fig = self.network.draw_graph_structure()
        canvas = FigureCanvasTkAgg(self.fig, master = self.win)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.win)
        toolbar.update()
        toolbar.place(x=600, y=20)
        canvas.get_tk_widget().place(x=200, y=70)