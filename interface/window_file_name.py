import os
import tkinter as tk

class FileNameWindow:
    def __init__(self, win, master):
        self.master=master
        self.win = win
        self.win.grab_set()
        self.win.focus_set()
        self.win.title('File name')
        self.win.geometry("400x150")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the json file name:')
        self.lbl_init_network.place(x=20, y=20)
        
        self.inputtxt_file = tk.Text(self.win,
                   height = 1,
                   width = 45)
        self.inputtxt_file.place(x=20, y=50)
        self.inputtxt_file.bind('<Return>', self.return_key)

        btn_enter = tk.Button(self.win,
                        text = "Enter", 
                        command = self.set_file_name)
        btn_enter.place(x=150, y=80)

        btn_cancel = tk.Button(self.win,
                        text = "Cancel", 
                        command = self.win.destroy)
        btn_cancel.place(x=200, y=80)

    def return_key(self, event):
        self.set_file_name()

    def set_file_name(self):
        current_dir = (f"{os.getcwd()}\data")
        file_name = self.inputtxt_file.get(1.0, "end-1c") # with .json extension
        path = (f"{current_dir}\{file_name}")

        self.master.create_network(file_name=path)
        self.win.destroy()