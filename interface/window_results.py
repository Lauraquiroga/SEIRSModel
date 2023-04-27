import tkinter as tk
from model.seirs_model import SEIRS_Model
from tkinter import messagebox

class ResultsWindow:
    def __init__(self, win, master, results:SEIRS_Model):
        self.master=master
        self.win = win
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

    def show_nw_evolution(self):
        """
        Pops a new window with the graph showing the
        evalution of the total amount of devices per compartment
        """
        pass

    def show_node_evolution(self):
        """
        Lets the user choose a node and visualize 
        the evolution of that device's probabilities
        """
        node = self.select_node()

    def select_node(self):
        pass

