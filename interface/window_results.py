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
                                          text = "See network evolution",
                                          command = self.show_nw_evolution)
        self.btn_nw_evolution.place(x=20, y=460)

        self.lbl_pick_node = tk.Label(win, text="Choose a device:")
        self.lbl_pick_node.place(x=190, y=460)

        nodes = [x for x in range(self.results.n)]
        self.cb_nodes=Combobox(win, values=nodes, state="readonly", width=10)
        self.cb_nodes.current(0)
        self.cb_nodes.place(x=290, y=460)

        self.btn_nd_evolution = tk.Button(self.win,
                                          text = "See node evolution",
                                          command = self.show_node_evolution)
        self.btn_nd_evolution.place(x=400, y=460)

        self.btn_save = tk.Button(self.win,
                                          text = "Save model results",
                                          command = self.save_results)
        self.btn_save.place(x=540, y=460)

        self.btn_restart = tk.Button(self.win,
                                          text = "Generate new model",
                                          command = self.restart)
        self.btn_restart.place(x=680, y=460)

    def show_nw_evolution(self):
        """
        Pops a new window with the graph showing the
        evalution of the total amount of devices per compartment
        """
        child_win = tk.Toplevel(self.win)
        child_win.title("Network evolution")
        fig = self.results.plot_network_evolution()
        self.show_plot(child_win, fig)

    def show_node_evolution(self):
        """
        Pops a new window with the graph showing 
        the evolution of the chosen device's probabilities
        """
        child_win = tk.Toplevel(self.win)
        child_win.title("Node evolution")
        node = int(self.cb_nodes.get())
        fig = self.results.plot_node_evolution(node)
        self.show_plot(child_win, fig)

    def show_plot(self, win, fig):
        """
        Draws the given figure (fig) in the given window (win)
        """
        canvas = FigureCanvasTkAgg(fig, master = win)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, win)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def save_results(self):
        """
        Save the model results in a json file
        """
        pass
    
    def restart(self):
        """
        Generate a new model
        """
        self.win.destroy()
        self.master.win.deiconify()