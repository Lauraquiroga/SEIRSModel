import tkinter as tk

class FileNameWindow:
    def __init__(self, win):
        self.win = win
        self.win.title('File name')
        self.win.geometry("400x150")
        self.win.resizable(0,0)

        self.lbl_init_network = tk.Label(win, text='Enter the json file name:')
        self.lbl_init_network.place(x=20, y=20)
        
        self.inputtxt_file = tk.Text(self.win,
                   height = 1,
                   width = 45)
        self.inputtxt_file.place(x=20, y=50)
        btn = tk.Button(self.win,
                        text = "Enter", 
                        command = self.test)
        btn.place(x=180, y=80)
        self.file_name=""

    def test(self):
        self.file_name=self.inputtxt_file.get(1.0, "end-1c")