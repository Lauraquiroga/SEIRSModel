import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model.seirs_model import SEIRS_Model

class HeatmapWindow:
    def __init__(self, win, master, results:SEIRS_Model):
        self.master = master
        self.win = win
        self.results = results
        self.win.title('SEIRS Model Results')
        x = 800
        y = 800
        self.win.geometry(f"{x}x{y}")
        self.win.resizable(0,0)

        self.lbl_title = tk.Label(win, text="NIMFA SEIRS Model - simulation")
        self.lbl_title.place(x=20, y=20)

        # Display heatmap
        self.show_heatmap()

        self.btn_save = tk.Button(self.win,
                                          text = "Save model results",
                                          command = self.save_results)
        self.btn_save.place(x=300, y=y-40)

        self.btn_restart = tk.Button(self.win,
                                          text = "Generate new model",
                                          command = self.restart)
        self.btn_restart.place(x=440, y=y-40)

        # Bind kill root to destroy event with close button
        self.win.protocol("WM_DELETE_WINDOW", self.kill_root)

    def show_heatmap(self):
        """
        Display heatmap with evolution of the network by initially infected device
        """
        self.fig = self.results.show_heatmap()
        canvas = FigureCanvasTkAgg(self.fig, master = self.win)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.win)
        toolbar.update()
        toolbar.place(x=400, y=20)
        canvas.get_tk_widget().place(x=100, y=70)

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