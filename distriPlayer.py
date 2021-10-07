#import needed libraries
import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

t = np.arange(0, 3, .01)
distributions = {"normal": 2 * np.sin(2 * np.pi * t), "t": 2 * np.sin(4 * np.pi * t), "beta": 2 * np.sin(50 * np.pi * t)}

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

        #configure buttons
        for plot in distributions:
            #add to sidebar
            button = tk.Button(self.sideBar)

            #add button text as distribution name
            button["text"] = plot

            #add button command to switch the plot
            button["command"] = lambda plot=plot: self.switch_plot(plot)

            #pack buttons
            button.pack(side="top")

        #configure frames which hold plots
        self.frames = {}
        for plot in distributions:

            frame = tk.Frame(self.mainView)
            # add canvas for mat plot
            fig = Figure(figsize=(5, 4), dpi=100)
            y = distributions[plot]
            fig.add_subplot(111).plot(y)

            canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            self.frames[plot] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_plot("normal")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def switch_plot(self,plot):
        frame = self.frames[plot]
        frame.tkraise()

def main():
    root = tk.Tk()
    root.wm_title("Distribution Player")
    player = d_player(master=root)
    player.mainloop()

if __name__ == "__main__":
    main()