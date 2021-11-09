#import needed libraries
import tkinter as tk
from tkinter import Checkbutton, ttk
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import math
import scipy.stats as stats
from scipy.special import factorial

#Array of all different types of distributions
distributions = ["normal","uniform","poison","beta","binomial","burr","chi-squared","exponential","extreme value",
                 "f","gamma","generalized extreme value","generalized pareto","geometric","half normal", "hypergeometric",
                 "lognormal", "negative binomial", "noncentral f", "noncentral t", "noncentral chi-squared", "rayleigh",
                 "stable", "t", "discret uniform", "weibull"]

class d_player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # add main view
        self.mainView = tk.Frame(self)
        self.mainView.pack(side="left")

        frame = tk.Frame(self)
        frame.pack(side=tk.RIGHT,fill=tk.BOTH)

        # #add sidebar
        # self.sideBar = tk.Frame(self)
        # self.sideBar.pack(side=tk.RIGHT,fill=tk.BOTH)
        # sidebar_width = self.sideBar.winfo_width()


        # #configure buttons
        # for plot in distributions:
        #     #add to sidebar
        #     button = tk.Button(self.sideBar)

        #     #add button text as distribution name
        #     button["text"] = plot

        #     #add button command to switch the plot
        #     button["command"] = lambda plot=plot: self.switch_plot(plot)

        #     #pack buttons
        #     button.pack(side="top",fill=tk.X)

                # distribution combobox
        dist = tk.Label(text = "distribution")
        dist.place(relx = 0.70, rely = 0.25, anchor = 'nw')

        selected_dist = tk.StringVar()
        dist_cb = ttk.Combobox(frame, textvariable = selected_dist, width = 20)
        dist_cb['values'] = distributions
        dist_cb['state'] = 'readonly'
        dist_cb.pack()
        # dist_cb.place(relx = 0.80, rely = 0.25, anchor = 'nw')

        # x range
        x_range = tk.Label(text = "x")
        x_range.place(relx = 0.70, rely = 0.35, anchor = 'nw')

        x_from = tk.Label(text = "from")
        x_from.place(relx = 0.80, rely = 0.35, anchor = 'nw')
        x_from_input = tk.Entry(width = 3)
        x_from_input.place(relx = 0.85, rely = 0.35, anchor = 'nw')

        x_to = tk.Label(text = "to")
        x_to.place(relx = 0.90, rely = 0.35, anchor = 'nw')
        x_to_input = tk.Entry(width = 3)
        x_to_input.place(relx = 0.95, rely = 0.35, anchor = 'nw')

        # parameters
        params = tk.Label(text = "parameters")
        params.place(relx = 0.70, rely = 0.45, anchor = 'nw')

        param_a = tk.Label(text = 'a')
        param_a.place(relx = 0.80, rely = 0.45, anchor = 'nw')
        param_a_input = tk.Entry(width = 3)
        param_a_input.place(relx = 0.85, rely = 0.45, anchor = 'nw')

        param_b = tk.Label(text = 'b')
        param_b.place(relx = 0.90, rely = 0.45, anchor = 'nw')
        param_b_input = tk.Entry(width = 3)
        param_b_input.place(relx = 0.95, rely = 0.45, anchor = 'nw')

        # log checkbox
        is_log = tk.Label(text = "log plot")
        is_log.place(relx = 0.70, rely = 0.55, anchor = 'nw')
        is_log_check_var = tk.IntVar()
        is_log_check = tk.Checkbutton(variable = is_log_check_var)
        is_log_check.place(relx = 0.80, rely = 0.55, anchor = 'nw')

        # plot button
        plot_button = tk.Button(text = "Plot!", width = 10)
        plot_button.place(relx = 0.80, rely = 0.65, anchor = 'nw')
        cb_input = dist_cb.get()
        print("here")
        print(cb_input)
        print("there")
        #dist_cb.bind('<<ComboboxSelected>>', self.switch_plot)
        plot_button["command"] = lambda plot=cb_input: self.switch_plot(plot)

        self.switch_plot(distributions[0])

        #self.quit = tk.Button(self.sideBar, text="QUIT", fg="red", command=self.master.destroy,)
        #self.quit.pack(side="bottom", fill=tk.X)

    def switch_plot(self,plot):

        for widget in self.mainView.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.mainView)

        # add canvas for mat plot
        fig = Figure(figsize=(5, 4), dpi=100)

        #plot the apropriate distribution
        if plot == "normal":
            mu = 0
            variance = 1
            sigma = math.sqrt(variance)
            x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
            y = stats.norm.pdf(x, mu, sigma)
            fig.add_subplot(111).plot(y)

        elif plot == "uniform":
            y = np.full(100,0.01)
            fig.add_subplot(111).plot(y)

        elif plot == "poison":
            t = np.arange(0, 3, .01)
            y = np.exp(-5)*np.power(5, t)/factorial(t)
            fig.add_subplot(111).plot(y)

        elif plot == "t":
            mu = 0
            variance = 1
            sigma = math.sqrt(variance)
            df = 2.74
            x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
            y = stats.t.pdf(x, df)
            fig.add_subplot(111).plot(y)

        elif plot == "beta":
            mu = 0
            variance = 1
            sigma = math.sqrt(variance)
            x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
            a = 2
            b = 2
            y = stats.beta.pdf(x,a,b, scale=100, loc=-50)
            fig.add_subplot(111).plot(y)
        else:
            t = np.arange(0, 3, .01)
            fig.add_subplot(111).plot(np.sin(2*np.pi*t))


        canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand=1)

        frame.pack(fill=tk.BOTH)
        # frame.grid(row=0, column=0, sticky="nsew")

def main():
    root = tk.Tk()
    root.wm_title("Distribution Player")
    root.geometry("1280x768")
    player = d_player(master=root)
    player.mainloop()

if __name__ == "__main__":
    main()