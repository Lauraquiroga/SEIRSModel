import tkinter as tk
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model.seirs_model import SEIRS_Model

class ResultsWindow:
    def __init__(self, win, master, results:SEIRS_Model):
        self.master = master
        self.win = win
        self.results = results
        self.win.title('SEIRS Model Results')
        self.win.geometry("1000x500")
        self.win.resizable(0,0)

        self.lbl_title = tk.Label(win, text="NIMFA SEIRS Model - simulation")
        self.lbl_title.place(x=20, y=20)

        self.btn_nw_evolution = tk.Button(self.win,
                                          text = "Network evolution",
                                          command = self.show_nw_evolution)
        self.btn_nw_evolution.place(x=20, y=460)

        self.btn_nd_evolution = tk.Button(self.win,
                                          text = "Node evolution",
                                          command = self.show_node_evolution)
        self.btn_nd_evolution.place(x=150, y=460)

        nodes = [x for x in range(self.results.n)]
        self.cb_nodes=Combobox(win, values=nodes, state="readonly")
        self.cb_nodes.current(0)
        self.cb_nodes.place(x=60, y=150)

    def show_nw_evolution(self):
        """
        Pops a new window with the graph showing the
        evalution of the total amount of devices per compartment
        """
        child_win = tk.Toplevel(self.win)
        child_win.title("Network evolution")
        fig = self.results.plot_network_evolution()
        canvas = FigureCanvasTkAgg(fig,
                            master = child_win)
    
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                    child_win)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def show_node_evolution(self):
        """
        Lets the user choose a node and visualize 
        the evolution of that device's probabilities
        """
        child_win = tk.Toplevel(self.win)
        child_win.title("Node evolution")
        node = int(self.cb_nodes.get())
        fig = self.results.plot_node_evolution(node)
        canvas = FigureCanvasTkAgg(fig,
                            master = child_win)
    
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                    child_win)
        toolbar.update()
        canvas.get_tk_widget().pack()
    
    def restart(self):
        """
        Generate a new model
        """
        self.win.destroy()
        self.master.win.deiconify()