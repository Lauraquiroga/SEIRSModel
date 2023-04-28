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
        y=800
        x=1000
        self.win.geometry(f"{x}x{y}")
        self.win.resizable(0,0)

        self.lbl_title = tk.Label(win, text="NIMFA SEIRS Model - simulation")
        self.lbl_title.place(x=20, y=20)

        self.current_step = len(self.results.nodes_comp)-1

        self.lbl_xts = tk.Label(win, text=f"{self.current_step*(self.results.resolution)} time step")
        self.lbl_xts.place(x=475, y=y-80)

        self.btn_back = tk.Button(self.win,
                                          text = "<",
                                          command = lambda:self.change_current_graph("back"))
        self.btn_back.place(x=425, y=y-80)

        self.btn_ford = tk.Button(self.win,
                                          text = ">",
                                          command =lambda:self.change_current_graph("ford"),
                                          state="disabled")
        
        self.btn_ford.place(x=560, y=y-80)

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
                                          text = "See node evolution",
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

        # Bind kill root to destroy event
        self.win.bind("<Destroy>", self.kill_root)

    def show_graph(self):
        self.fig = self.results.show_graph(self.current_step)
        canvas = FigureCanvasTkAgg(self.fig, master = self.win)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.win)
        toolbar.update()
        toolbar.place(x=600, y=20)
        canvas.get_tk_widget().place(x=200, y=70)

    def change_current_graph(self, direction:str):
        self.fig.clear()
        if(direction=="back"):
            self.current_step-=1
            print(self.current_step)
        else:
            self.current_step+=1
        # Update time step label
        self.lbl_xts.config(text=f"{self.current_step*(self.results.resolution)} time step")
        # Disable buttons to avoid OOR
        """
        if (self.current_step==0):
            self.btn_back["state"]="disabled"
        elif (self.current_step==1):
            self.btn_back["state"]="normal"
        
        if (self.current_step==len(self.results.nodes_comp)-1):
            self.btn_back["state"]="disabled"
        elif (self.current_step==len(self.results.nodes_comp)-2):
            self.btn_back["state"]="normal"
        """
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
        pass
    
    def restart(self):
        """
        Generate a new model
        """
        self.win.destroy()
        self.master.win.deiconify()

    def kill_root(self, event):
        """
        Destroys master window on close
        """
        if event.widget == self.win and self.master.win.winfo_exists():
            self.master.win.destroy()