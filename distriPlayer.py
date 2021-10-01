import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class d_player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.type = "normal"

        #add sidebar
        self.sideBar = tk.Frame(self)
        self.sideBar.pack(side="right")

        #add main view
        self.mainView = tk.Frame(self)
        self.mainView.pack(side="left")

        #add buttons to sidbar
        self.normal = tk.Button(self.sideBar)
        self.t = tk.Button(self.sideBar)
        self.binomial = tk.Button(self.sideBar)

        #configure buttons
        self.normal["text"] = "Normal Distribution"
        self.t["text"] = "t Distribution"
        self.binomial["text"] = "binomial Distribution"

        self.normal["command"] = lambda: self.create_plot("normal")
        self.t["command"] = lambda: self.create_plot("t")
        self.binomial["command"] = lambda: self.create_plot("binomial")

        #place buttons
        self.normal.pack(side="top")
        self.t.pack(side="top")
        self.binomial.pack(side="top")

        #add canvas for mat plot
        self.draw_plot(self.mainView)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def create_plot(self,type2):
        self.type = type2
        self.draw_plot(self.mainView)

    def draw_plot(self, parent):
        t = np.arange(0, 3, .01)
        get_plot = {"normal": 2 * np.sin(2 * np.pi * t), "t": 2 * np.sin(4 * np.pi * t), "binomial":2 * np.sin(50 * np.pi * t)}

        # add canvas for mat plot
        fig = Figure(figsize=(5, 4), dpi=100)
        y = get_plot[self.type]
        fig.add_subplot(111).plot(t, y)

        self.canvas = FigureCanvasTkAgg(fig, master=parent)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


root = tk.Tk()
root.wm_title("Distribution Player")
player = d_player(master=root)
player.mainloop()