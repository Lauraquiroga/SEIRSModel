import tkinter as tk

class InitialWindow:
    def __init__(self, win):
        self.win = win
        self.lbl_init_network = tk.Label(win, text='Select how to initialize the network')
        self.lbl_init_network.place()
        self.btn_load_prob = tk.Button(win, text='Load network with initial probabilities from file', command=self.load_file_prob)
        self.btn_load_noprob = tk.Button(win, text='Load network structure from file (no initial probabilities)', command=self.load_file_noprob)
        self.btn_generate_new = tk.Button(win, text='Generate new random network', command=self.generate_network)
        self.btn_load_prob.place()
        self.btn_load_noprob.place()
        self.btn_generate_new.place()

    def load_file_prob(self):
        print(1)

    def load_file_noprob(self):
        print(2)

    def generate_network(self):
        print(3)

def main(): 
    root = tk.Tk()
    root.title("SEIRS Model")
    root.geometry("350x350")
    root.resizable(0,0)
    InitialWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()