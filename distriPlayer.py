#import needed libraries
import tkinter as tk
from tkinter import Checkbutton, ttk
from tkinter.constants import BOTTOM, RIGHT
import numpy as np
import matplotlib as mpl
# import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import math
import scipy.stats as stats
from scipy.special import factorial

#Import specific distributions
#Some inconsistencies between importing scipy as ss vs. stats
import scipy.stats as ss
from scipy.special import factorial
from scipy.stats import beta
from scipy.stats import binom
from scipy.stats import burr
from scipy.stats import chi2
from scipy.stats import gumbel_l
from scipy.stats import f
from scipy.stats import gamma
from scipy.stats import genextreme
from scipy.stats import genpareto
from scipy.stats import geom
from scipy.stats import halfnorm
from scipy.stats import hypergeom
from scipy.stats import lognorm
from scipy.stats import nbinom
from scipy import special
from scipy.stats import t as t_dist
from scipy.stats import ncx2
from scipy.stats import rayleigh
from scipy.stats import levy_stable
from scipy.stats import randint
from scipy.stats import weibull_min

#Array of all different types of distributions
distributions = ["normal","uniform","poison","beta","binomial","burr","chi-squared","exponential","extreme value",
                 "f","gamma","generalized extreme value","generalized pareto","geometric","half normal", "hypergeometric",
                 "lognormal", "negative binomial", "noncentral f", "noncentral t", "noncentral chi-squared", "rayleigh",
                 "stable", "t", "discret uniform", "weibull"]

class d_player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.pack()
        self.create_widgets()

    def get_dist(self,event):
        self.selected = self.dist_cb.get()
        print(self.dist_cb.get())

        # plot button
        self.plot_button = tk.Button(text="Plot!", width=10)
        self.plot_button.grid(column=1, row=11)
        # self.plot_button.place(relx=0.80, rely=0.65, anchor='nw')
        # cb_input = dist_cb.get()
        # dist_cb.bind('<<ComboboxSelected>>', self.switch_plot)
        self.plot_button["command"] = lambda plot=self.dist_cb.get(): self.switch_plot(plot)
        # self.switch_plot(dist_cb.get())
        # cb_input = dist_cb.get()
        return self.dist_cb.get()

    def create_widgets(self):

       # add main view
       self.mainView = tk.Frame(self)
       self.mainView.pack(side="left")

       frame = tk.Frame(self)
       frame.pack(side=tk.RIGHT, fill=tk.BOTH)

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
       self.dist = tk.Label(text="distribution")
       self.dist.grid(column=1,row=0)
       # self.dist.place(relx=0.70, rely=0.25, anchor='nw')

       self.selected_dist = tk.StringVar()
       # self.dist_cb = ttk.Combobox(frame, textvariable=self.selected_dist, width=20)
       self.dist_cb = ttk.Combobox(textvariable=self.selected_dist, width=20)
       self.dist_cb['values'] = distributions
       self.dist_cb['state'] = 'readonly'

       self.dist_cb.bind('<<ComboboxSelected>>', self.get_dist)
       self.dist_cb.grid(column=1,row=1)
       # self.dist_cb.pack(pady=300)

       #x range
       self.x_range = tk.Label(text="x")
       self.x_range.grid(column=1,row=3)
       # self.x_range.place(relx=0.70, rely=0.35, anchor='nw')

       self.x_from = tk.Label(text="from")
       self.x_from.grid(column=1,row=4)
       # self.x_from.place(relx=0.80, rely=0.35, anchor='nw')
       self.x_from_input = tk.Entry(width=3)
       self.x_from_input.grid(column=2, row=4)
       # self.x_from_input.place(relx=0.85, rely=0.35, anchor='nw')

       self.x_to = tk.Label(text="to")
       self.x_to.grid(column=3, row=4)
       # self.x_to.place(relx=0.90, rely=0.35, anchor='nw')
       self.x_to_input = tk.Entry(width=3)
       self.x_to_input.grid(column=4, row=4)
       # self.x_to_input.place(relx=0.95, rely=0.35, anchor='nw')

       # parameters
       # self.param_frame = tk.Frame(self,width=1000, height=600)
       # self.param_frame.grid(column=1, row=6)
       # self.param_frame.place(relx=0, rely=0.9, anchor='nw')

       #delete old parameter values
       # for widget in self.param_frame.winfo_children():
       #     widget.destroy()

       self.param_list = ['a', 'b', 'c', 'd','e','f']
       for i,param in enumerate(self.param_list):
           new_label = tk.Label(text=param)
           new_label.grid(column=2*i+1, row=7)
           new_box = tk.Entry(width=2)
           new_box.grid(column=2*i+2, row=7)

       # self.param_a = tk.Label(self.param_frame,text='a')
       # self.param_a.pack(side=tk.LEFT)
       # self.param_b = tk.Label(self.param_frame, text='a')
       # self.param_b.pack(side=tk.LEFT)
       # self.param_c = tk.Label(self.param_frame, text='a')
       # self.param_c.pack(side=tk.LEFT)

       # self.params = tk.Label(text="parameters")
       # self.params.place(relx=0.70, rely=0.45, anchor='nw')
       #
       # self.param_a = tk.Label(text='a')
       # self.param_a.place(relx=0.80, rely=0.45, anchor='nw')
       # self.param_a_input = tk.Entry(width=3)
       # self.param_a_input.place(relx=0.85, rely=0.45, anchor='nw')
       #
       # self.param_b = tk.Label(text='b')
       # self.param_b.place(relx=0.90, rely=0.45, anchor='nw')
       # self.param_b_input = tk.Entry(width=3)
       # self.param_b_input.place(relx=0.95, rely=0.45, anchor='nw')

       # log checkbox
       self.is_log = tk.Label(text="log plot")
       self.is_log.grid(column=1, row=9)
       # self.is_log.place(relx=0.70, rely=0.55, anchor='nw')
       self.is_log_check_var = tk.IntVar()
       self.is_log_check = tk.Checkbutton(variable=self.is_log_check_var)
       self.is_log_check.grid(column=1, row=10)
       # self.is_log_check.place(relx=0.80, rely=0.55, anchor='nw')

       # plot button
       # plot_button = tk.Button(text = "Plot!", width = 10)
       # plot_button.place(relx = 0.80, rely = 0.65, anchor = 'nw')
       # cb_input = dist_cb.get()
       # dist_cb.bind('<<ComboboxSelected>>', self.switch_plot)
       # plot_button["command"] = lambda plot=cb_input: self.switch_plot(plot)

       # self.switch_plot(cb_input)

       # self.quit = tk.Button(self.sideBar, text="QUIT", fg="red", command=self.master.destroy,)
       # self.quit.pack(side="bottom", fill=tk.X)

    def switch_plot(self,plot):

        for widget in self.mainView.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.mainView)

        # add canvas for mat plot
        fig = Figure(figsize=(5, 4), dpi=100)

        # #plot the apropriate distribution
        # if plot == "normal":
        #     mu = 0
        #     variance = 1
        #     sigma = math.sqrt(variance)
        #     x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        #     y = stats.norm.pdf(x, mu, sigma)
        #
        #
        #     # make an image plot
        #     ax =  fig.add_subplot(111)
        #     ax.plot(x,y)
        #
        # elif plot == "uniform":
        #     y = np.full(100,0.01)
        #     ax = fig.add_subplot(111)
        #     ax.plot(y)
        #
        # elif plot == "poison":
        #     t = np.arange(0, 3, .01)
        #     y = np.exp(-5)*np.power(5, t)/factorial(t)
        #     ax = fig.add_subplot(111)
        #     ax.plot(t,y)
        #
        # elif plot == "t":
        #     mu = 0
        #     variance = 1
        #     sigma = math.sqrt(variance)
        #     df = 2.74
        #     x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        #     y = stats.t.pdf(x, df)
        #     ax = fig.add_subplot(111)
        #     ax.plot(x, y)
        #
        # elif plot == "beta":
        #     mu = 0
        #     variance = 1
        #     sigma = math.sqrt(variance)
        #     x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        #     a = 2
        #     b = 2
        #     y = stats.beta.pdf(x,a,b, scale=100, loc=-50)
        #     ax = fig.add_subplot(111)
        #     ax.plot(x, y)

        a = 0
        b = 1
        xmin = 0
        xmax = 1

        ax = fig.add_subplot(111)

        if plot == "normal":
            # a: mu
            # b: variance
            sigma = math.sqrt(b)
            x = np.linspace(a - 3 * sigma, a + 3 * sigma, 100)
            y = stats.norm.pdf(x, a, sigma)
            ax.plot(x, y, label="Normal Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "uniform":
            y = 1
            x = np.arange(0, 1)
            ax.hlines(y, xmin=0, xmax=1, linewidth=4)
            ax.hlines(0, xmin=-.5, xmax=a, linewidth=4)
            ax.hlines(0, xmin=b, xmax=1.5, linewidth=4)
            ax.vlines(a, ymin=0, ymax=y, linewidth=4)
            ax.vlines(b, ymin=0, ymax=y, linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "poisson":
            # a: mu
            # b: n/a
            x = np.arange(0, 20, 0.1)
            y = np.exp(-a) * np.power(a, x) / factorial(x)
            ax.plot(x, y, label="Poisson Distribution", linewidth=5)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "beta":
            # a: alpha
            # b: beta
            x = np.arange(-50, 50, 0.1)
            y = beta.pdf(x, a, b, scale=100, loc=-50)
            ax.plot(x, y, label="Beta Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "binomial":
            # a: n
            # b: p
            x = np.arange(binom.ppf(0.001, a, b),
                          binom.ppf(0.999, a, b))
            y = binom.pmf(x, a, b)
            ax.plot(x, y, label="Binomial Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "burr":
            # a: c
            # b: d
            x = np.linspace(burr.ppf(0.01, a, b),
                            burr.ppf(0.99, a, b), 100)
            y = burr.pdf(x, a, b)
            ax.plot(x, y, label="Burr Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "chi-squared":
            # a: k (degrees of freedom)
            # b: N/A
            x = np.arange(0, 20, 0.001)
            y = chi2.pdf(x, df=a)
            ax.plot(x, y, label="Chi-squared distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "exponential":
            # a: mu
            # b: sigma
            x = np.arange(0, 20, 0.001)
            y = ss.expon.pdf(x, a, b)
            ax.plot(x, y, label="Exponential Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "extreme value":
            # a: ???
            # b: ???
            mean, var, skew, kurt = gumbel_l.stats(moments='mvsk')
            x = np.linspace(gumbel_l.ppf(0.01),
                            gumbel_l.ppf(0.99), 100)
            y = gumbel_l.pdf(x)
            ax.plot(x, y, label="Extreme Value Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "f":
            # a: v1
            # b: v2
            mean, var, skew, kurt = f.stats(a, b, moments='mvsk')
            x = np.linspace(f.ppf(0.01, a, b),
                            f.ppf(0.99, a, b), 100)
            y = f.pdf(x, a, b)
            ax.plot(x, y, label="F Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "gamma":
            # a: k
            # b: ??? (shouldn't there be two?)
            mean, var, skew, kurt = gamma.stats(a, moments='mvsk')
            x = np.linspace(gamma.ppf(0.01, a),
                            gamma.ppf(0.99, a), 100)
            y = gamma.pdf(x, a)
            ax.plot(x, y, label="Gamma Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "generalized extreme value":
            # a: c
            # b: ???
            mean, var, skew, kurt = genextreme.stats(a, moments='mvsk')
            x = np.linspace(genextreme.ppf(0.01, a),
                            genextreme.ppf(0.99, a), 100)
            y = genextreme.pdf(x, a)
            ax.plot(x, y, label="Generalized Extreme Value Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "generalized pareto":
            # a: c
            # b: ???
            mean, var, skew, kurt = genpareto.stats(a, moments='mvsk')
            x = np.linspace(genpareto.ppf(0.01, a),
                            genpareto.ppf(0.99, a), 100)
            y = genpareto.pdf(x, a)
            ax.plot(x, y, label="Generalized Pareto Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "geometric":
            # a: p
            # b: ???
            mean, var, skew, kurt = geom.stats(a, moments='mvsk')
            x = np.arange(geom.ppf(0.01, a),
                          geom.ppf(0.99, a))
            y = geom.pmf(x, a)
            ax.plot(x, y, label="Geometric Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "half normal":
            # a: ??? No paremeters ???
            # b: ???
            mean, var, skew, kurt = halfnorm.stats(moments='mvsk')
            x = np.linspace(halfnorm.ppf(0.01),
                            halfnorm.ppf(0.99), 100)
            y = halfnorm.pdf(x)
            ax.plot(x, y, label="Half-normal Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "hypergeometric":
            # a: M
            # b: n
            # c: N
            # There are three parameters for hypergeometric distributions,
            # but we are setting sample size as a constant
            N = 15
            rv = hypergeom(a, b, N)
            x = np.arange(0, b + 1)
            y = rv.pmf(x)
            ax.plot(x, y, label="Hypergeometric Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "lognormal":
            # a: s
            # b: ???
            mean, var, skew, kurt = lognorm.stats(a, moments='mvsk')
            x = np.linspace(lognorm.ppf(0.01, a),
                            lognorm.ppf(0.99, a), 100)
            y = lognorm.pdf(x, a)
            ax.plot(x, y, label="Lognormal Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "negative binomial":
            # a: n
            # b: p
            mean, var, skew, kurt = nbinom.stats(a, b, moments='mvsk')
            x = np.arange(nbinom.ppf(0.01, a, b),
                          nbinom.ppf(0.99, a, b))
            y = nbinom.pmf(x, a, b)
            ax.plot(x, y, label="Negative Binomial Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "noncentral f":
            # a: dfn
            # b: dfd
            x = np.linspace(-1, 8, num=500)
            y = stats.f.cdf(x, a, b)
            ax.plot(x, y, label="Noncentral F Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "noncentral t":
            # a: df
            # b: ???
            mean, var, skew, kurt = t.stats(a, moments='mvsk')
            x = np.linspace(t.ppf(0.01, a),
                            t.ppf(0.99, a), 100)
            y = t.pdf(x, a)
            ax.plot(x, y, label="Noncentral t Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "noncentral chi-squared":
            # a: df
            # b: nc
            mean, var, skew, kurt = ncx2.stats(a, b, moments='mvsk')
            x = np.linspace(ncx2.ppf(0.01, a, b),
                            ncx2.ppf(0.99, a, b), 100)
            y = ncx2.pdf(x, a, b)
            ax.plot(x, y, label="Noncentral Chi-squared Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "rayleigh":
            # a: ??? No parameters ???
            # b: ???
            mean, var, skew, kurt = rayleigh.stats(moments='mvsk')
            x = np.linspace(rayleigh.ppf(0.01),
                            rayleigh.ppf(0.99), 100)
            y = rayleigh.pdf(x)
            ax.plot(x, y, label="Rayleigh Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "stable":
            # a: alpha
            # b: beta
            mean, var, skew, kurt = levy_stable.stats(a, b, moments='mvsk')
            x = np.linspace(levy_stable.ppf(0.01, a, b),
                            levy_stable.ppf(0.99, a, b), 100)
            y = levy_stable.pdf(x, a, b)
            ax.plot(x, y, label="Stable Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "t":
            # a: df
            # b: ???
            mean, var, skew, kurt = t_dist.stats(a, moments='mvsk')
            x = np.linspace(t_dist.ppf(0.01, a),
                            t_dist.ppf(0.99, a), 100)
            y = t_dist.pdf(x, a)
            ax.plot(x, y, label="t Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        elif plot == "discrete uniform":
            # a: low
            # b: high
            mean, var, skew, kurt = randint.stats(a, b, moments='mvsk')
            x = np.arange(randint.ppf(0.01, a, b),
                          randint.ppf(0.99, a, b))
            y = randint.pmf(x, a, b)
            fig, ax = ax.subplots(1, 1)
            ax.plot(x, y, label="Discrete Uniform Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.vlines(x, 0, randint.pmf(x, a, b))
            ax.set_xlim([xmin, xmax])

        elif plot == "weibull":
            # a: c
            # b: ???
            mean, var, skew, kurt = weibull_min.stats(a, moments='mvsk')
            x = np.linspace(weibull_min.ppf(0.01, a),
                            weibull_min.ppf(0.99, a), 100)
            y = weibull_min.pdf(x, a)
            ax.plot(x, y, label="Weibull Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.set_xlim([xmin, xmax])

        else:
            t = np.arange(0, 3, .01)
            ax = fig.add_subplot(111)
            ax.plot(np.sin(2*np.pi*t))

        canvas = FigureCanvasTkAgg(fig)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(column=0,row=0)
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand=1)

        # frame.pack(fill=tk.BOTH)
        # frame.grid(row=0, column=0, sticky="nsew")

def main():
    root = tk.Tk()
    root.wm_title("Distribution Player")
    # root.geometry("1000x600")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)
    root.resizable(False,False)
    root.update_idletasks()
    player = d_player(master=root)
    player.mainloop()
if __name__ == "__main__":
    main()