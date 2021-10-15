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
        #add sidebar
        self.sideBar = tk.Frame(self,width=150)
        self.sideBar.pack(side="right")
        sidebar_width = self.sideBar.winfo_width()
        print(sidebar_width)

        #add main view
        self.mainView = tk.Frame(self)
        self.mainView.pack(side="left")

        #configure buttons
        for plot in distributions:
            #add to sidebar
            button = tk.Button(self,width=sidebar_width,height=2)

            #add button text as distribution name
            button["text"] = plot

            #add button command to switch the plot
            button["command"] = lambda plot=plot: self.switch_plot(plot)

            #pack buttons
            button.pack(side="top")

        self.switch_plot(list(distributions.keys())[0])

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy,width=sidebar_width,height=2)
        self.quit.pack(side="bottom")

    def switch_plot(self,plot):

        for widget in self.mainView.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.mainView)

        # add canvas for mat plot
        fig = Figure(figsize=(5, 4), dpi=100)
        y = distributions[plot]
        fig.add_subplot(111).plot(y)

        canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        frame.grid(row=0, column=0, sticky="nsew")

def main():
    root = tk.Tk()
    root.wm_title("Distribution Player")
    root.geometry("800x400")
    player = d_player(master=root)
    player.mainloop()

if __name__ == "__main__":
    main()