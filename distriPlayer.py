#import needed libraries
import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import math
import scipy.stats as stats
from scipy.special import factorial

t = np.arange(0, 3, .01)

#needed variables
mu = 0
variance = 1
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
a = 2
b = 2
n, p = 5, 0.4
df = 2.74
mean, var, skew, kurt = stats.t.stats(df, moments='mvsk')

distributions = {"normal": stats.norm.pdf(x, mu, sigma), "uniform": np.full(100,0.01), "poison": np.exp(-5)*np.power(5, t)/factorial(t),"t": stats.t.pdf(x, df), "beta": stats.beta.pdf(x,a,b, scale=100, loc=-50)}

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