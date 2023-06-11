import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model.seirs_model import SEIRS_Model
from model.states import States

class ResultsWindow:
    def __init__(self, win, master, results:SEIRS_Model):
        self.master = master
        self.win = win
        self.results = results
        self.win.title('SEIRS Model Results')
        y=800
        x=1000
        self.win.geometry(f"{x}x{y}")
        self.win.resizable(0,0)

        self.lbl_title = tk.Label(win, text="NIMFA SEIRS Model - simulation")
        self.lbl_title.place(x=20, y=20)

        self.current_step = len(self.results.nodes_comp)-1

        self.lbl_xts = tk.Label(win, text=f"{self.current_step*0.5} time step")
        self.lbl_xts.place(x=475, y=y-80)

        self.btn_first = tk.Button(self.win,
                                          text = "|<",
                                          command = lambda:self.change_current_graph("first"))
        self.btn_first.place(x=400, y=y-80)

        self.btn_back = tk.Button(self.win,
                                          text = "<",
                                          command = lambda:self.change_current_graph("back"))
        self.btn_back.place(x=425, y=y-80)

        self.btn_ford = tk.Button(self.win,
                                          text = ">",
                                          command =lambda:self.change_current_graph("ford"),
                                          state="disabled")
        self.btn_ford.place(x=560, y=y-80)

        self.btn_last = tk.Button(self.win,
                                          text = ">|",
                                          command = lambda:self.change_current_graph("last"),
                                          state="disabled")
        self.btn_last.place(x=585, y=y-80)

        # Display graph
        self.show_graph()

        self.btn_nw_evolution = tk.Button(self.win,
                                          text = "See network evolution",
                                          command = self.show_nw_evolution)
        self.btn_nw_evolution.place(x=110, y=y-40)

        self.lbl_pick_node = tk.Label(win, text="Choose a device:")
        self.lbl_pick_node.place(x=280, y=y-40)

        nodes = [x for x in range(self.results.n)]
        self.cb_nodes=Combobox(win, values=nodes, state="readonly", width=10)
        self.cb_nodes.current(0)
        self.cb_nodes.place(x=380, y=y-40)

        self.btn_nd_evolution = tk.Button(self.win,
                                          text = "See device evolution",
                                          command = self.show_node_evolution)
        self.btn_nd_evolution.place(x=480, y=y-40)

        self.btn_save = tk.Button(self.win,
                                          text = "Save model results",
                                          command = self.save_results)
        self.btn_save.place(x=640, y=y-40)

        self.btn_restart = tk.Button(self.win,
                                          text = "Generate new model",
                                          command = self.restart)
        self.btn_restart.place(x=780, y=y-40)

        # Bind kill root to destroy event with close button
        self.win.protocol("WM_DELETE_WINDOW", self.kill_root)

    def show_graph(self):
        """
        Display network with coloured nodes depending on 
        compartments at current step
        """
        self.fig = self.results.show_graph(self.current_step)
        canvas = FigureCanvasTkAgg(self.fig, master = self.win)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.win)
        toolbar.update()
        toolbar.place(x=600, y=20)
        canvas.get_tk_widget().place(x=200, y=70)

    def change_current_graph(self, direction:str):
        """
        Move in direction (backwards or forwards) in time 
        of the simulation to change graph visualization
        """
        
        self.fig.clear()
        if(direction=="back"):
            self.current_step-=1
        elif(direction=="ford"):
            self.current_step+=1
        elif(direction=="first"):
            self.current_step=0
        else:
            self.current_step=len(self.results.nodes_comp)-1

        # Update time step label
        self.lbl_xts.config(text=f"{self.current_step*0.5} time step")

        # Disable buttons to avoid index out of range
        if (self.current_step==0):
            self.btn_back["state"]="disabled"
            self.btn_first["state"]="disabled"
        else:
            self.btn_back["state"]="normal"
            self.btn_first["state"]="normal"
        
        if (self.current_step==len(self.results.nodes_comp)-1):
            self.btn_ford["state"]="disabled"
            self.btn_last["state"]="disabled"
        else:
            self.btn_ford["state"]="normal"
            self.btn_last["state"]="normal"
        
        self.show_graph()

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
        # Get the current datetime
        current_datetime = datetime.now()
        # Format the datetime as YYYYMMDDhhmmss
        formatted_time = current_datetime.strftime("%Y%m%d%H%M%S")

        #Create customized JSON structure
        totals_list = self.results.totals.tolist()
        prob_s = self.results.x.tolist()
        prob_e = self.results.w.tolist()
        prob_i = self.results.y.tolist()
        prob_r = self.results.z.tolist()
        probs=[]
        for node in range(self.results.n):
            probs.append({"node":node,
                         "S": prob_s[node],
                         "E": prob_e[node],
                         "I": prob_i[node],
                         "R": prob_r[node]})
        output= {
            "totals": {
                "S": totals_list[States.S.value],
                "E": totals_list[States.E.value],
                "I": totals_list[States.I.value],
                "R": totals_list[States.R.value]
            },
            "probabilities": probs
        }

        # Define the output file path
        current_dir = (f"{os.getcwd()}\data\\results")
        output_file = f"probs{self.results.n}n{self.results.rates['beta']*100}-{self.results.rates['alpha']*100}-{self.results.rates['delta']*100}-{self.results.rates['gamma']*100}rates{formatted_time}.json"
        path = (f"{current_dir}\\{output_file}")

        with open(path, "w") as file:
            json.dump(output, file)

        messagebox.showinfo(message=f"The model results have been saved in the '{output_file}' file in the data\\results folder", title="Saved")
        self.btn_save["state"]="disabled"

    def restart(self):
        """
        Generate a new model
        """
        self.master.win.deiconify()
        self.win.destroy()

    def kill_root(self):
        """
        Destroys master window on close
        """
        if self.master.win.winfo_exists():
            self.master.win.destroy()