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
from scipy.stats import nct
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

#dictionary to retreive parameter dictionary from distribution name
d_to_param = {
"normal":{'mu': 0, 'sigma': 1},
"uniform":{'a': 0, 'b':1},
"poison":{'mu':5},
"beta":{'a':2,'b':2},
"binomial":{'n':20,'p':0.5},
"burr":{'c':10,'d':5},
"chi-squared":{'k':4,'location':0},
"exponential":{'mu':1,'sigma':1},
"extreme value":{'location':0,'scale':5},
"f":{'v1':30,'v2':20},
"gamma":{'k':2,'theta':2},
"generalized extreme value":{'c':-0.1,'scale':1},
"generalized pareto":{'c':0.1,'scale':1},
"geometric":{'p':0.5,'location':0},
"half normal":{'location':0,'scale':1},
"hypergeometric":{'M':20,'n':7,'N':15},
"lognormal":{'sigma':0.95,'scale':1},
"negative binomial":{'n':5,'p':0.5},
"noncentral f":{'dfn':3,'dfd':2},
"noncentral t":{'df':3,'nc':1},
"noncentral chi-squared":{'df':20,'nc':1},
"rayleigh":{'scale':1,'location':0},
"stable":{'alpha':2,'beta':-0.5},
"t":{'df':3,'scale':1},
"discret uniform":{'low':5,'high':20},
"weibull":{'c':2,'scale':1}
}

class d_player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def get_dist(self,event):
        #get selected value
        self.dist_cb.get()

        #remove old parameter labels
        for label in self.param_label:
            self.param_label[label].grid_remove()

        #remove old entries
        for entry in self.param_entry:
            self.param_entry[entry].grid_remove()

        #set dictionary of parameters
        self.param_dic = d_to_param[self.dist_cb.get()]

        #update parameters gui
        self.param_entry = {}
        self.param_label = {}
        for i, lab in enumerate(self.param_dic):
            self.param_label[lab] = tk.Label(text=lab)
            self.param_label[lab].grid(column=2 * i + 2, row=4)
            self.param_entry[lab] = tk.Entry(width=2)
            self.param_entry[lab].insert(0, self.param_dic[lab])
            self.param_entry[lab].grid(column=2 * i + 3, row=4)

        #creat plot button
        self.plot_button = tk.Button(text="Plot!", width=10)
        self.plot_button.grid(column=1, row=6)

        self.plot_button["command"] = lambda plot=self.dist_cb.get(): self.switch_plot(plot)

        return self.dist_cb.get()

    def create_widgets(self):

        # distribution combobox
        self.dist = tk.Label(text="distribution")
        self.dist.grid(column=1,row=0)

        self.selected_dist = tk.StringVar()
        self.dist_cb = ttk.Combobox(textvariable=self.selected_dist, width=20)
        self.dist_cb['values'] = distributions
        self.dist_cb['state'] = 'readonly'

        self.dist_cb.bind('<<ComboboxSelected>>', self.get_dist)
        self.dist_cb.grid(column=1,row=1)

        #x range
        self.x_range = tk.Label(text="x")
        self.x_range.grid(column=1,row=3)

        self.x_from = tk.Label(text="from")
        self.x_from.grid(column=2,row=3)
        self.x_from_input = tk.Entry(width=3)
        self.x_from_input.insert(0,0)
        self.x_from_input.grid(column=3, row=3)

        self.x_to = tk.Label(text="to")
        self.x_to.grid(column=4, row=3)
        self.x_to_input = tk.Entry(width=3)
        self.x_to_input.insert(0,1)
        self.x_to_input.grid(column=5, row=3)

        #parameters
        self.param_lbl = tk.Label(text="parameters")
        self.param_lbl.grid(column=1,row=4)
        self.param_entry = {}
        self.param_label = {}

        # log checkbox
        self.is_log = tk.Label(text="log plot")
        self.is_log.grid(column=1, row=5)
        self.is_log_check_var = tk.IntVar()
        self.is_log_check = tk.Checkbutton(variable=self.is_log_check_var)
        self.is_log_check.grid(column=2, row=5)

    def switch_plot(self,plot):

        # add canvas for mat plot
        fig = Figure(figsize=(5, 4), dpi=100)

        ax = fig.add_subplot(111)

        if plot == "normal":
            a = self.param_dic['mu']
            sigma = self.param_dic['sigma']
            x = np.linspace(a - 3 * sigma, a + 3 * sigma, 100)
            y = stats.norm.pdf(x, a, sigma)
            ax.plot(x, y, label="Normal Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "uniform":
            y = 1
            a = self.param_dic['a']
            b = self.param_dic['b']
            ax.hlines(y, xmin=0, xmax=1, linewidth=4)
            ax.hlines(0, xmin=-.5, xmax=a, linewidth=4)
            ax.hlines(0, xmin=b, xmax=1.5, linewidth=4)
            ax.vlines(a, ymin=0, ymax=y, linewidth=4)
            ax.vlines(b, ymin=0, ymax=y, linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "poisson":
            a = self.param_dic['mu']
            x = np.arange(0, 20, 0.1)
            y = np.exp(-a) * np.power(a, x) / factorial(x)
            ax.plot(x, y, label="Poisson Distribution", linewidth=5)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "beta":
            a = self.param_dic['a']
            b = self.param_dic['b']
            x = np.arange(-50, 50, 0.1)
            y = beta.pdf(x, a, b, scale=100, loc=-50)
            ax.plot(x, y, label="Beta Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "binomial":
            a = self.param_dic['n']
            b = self.param_dic['p']
            x = np.arange(binom.ppf(0.001, a, b),
                          binom.ppf(0.999, a, b))
            y = binom.pmf(x, a, b)
            ax.plot(x, y, label="Binomial Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "burr":
            a = self.param_dic['c']
            b = self.param_dic['d']
            x = np.linspace(burr.ppf(0.01, a, b),
                            burr.ppf(0.99, a, b), 100)
            y = burr.pdf(x, a, b)
            ax.plot(x, y, label="Burr Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "chi-squared":
            a = self.param_dic['k']
            x = np.arange(0, 20, 0.001)
            y = chi2.pdf(x, df=a)
            ax.plot(x, y, label="Chi-squared distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "exponential":
            a = self.param_dic['mu']
            b = self.param_dic['sigma']
            x = np.arange(0, 20, 0.001)
            y = ss.expon.pdf(x, a, b)
            ax.plot(x, y, label="Exponential Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "extreme value":
            a = self.param_dic['location']
            b = self.param_dic['scale']
            mean, var, skew, kurt = gumbel_l.stats(moments='mvsk')
            x = np.linspace(gumbel_l.ppf(0.01),
                            gumbel_l.ppf(0.99), 100)
            y = gumbel_l.pdf(x)
            ax.plot(x, y, label="Extreme Value Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "f":
            a = self.param_dic['v1']
            b = self.param_dic['v2']
            mean, var, skew, kurt = f.stats(a, b, moments='mvsk')
            x = np.linspace(f.ppf(0.01, a, b),
                            f.ppf(0.99, a, b), 100)
            y = f.pdf(x, a, b)
            ax.plot(x, y, label="F Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "gamma":
            a = self.param_dic['k']
            b = self.param_dic['theta']
            mean, var, skew, kurt = gamma.stats(a, moments='mvsk')
            x = np.linspace(gamma.ppf(0.01, a),
                            gamma.ppf(0.99, a), 100)
            y = gamma.pdf(x, a)
            ax.plot(x, y, label="Gamma Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "generalized extreme value":
            a = self.param_dic['c']
            b = self.param_dic['scale']
            mean, var, skew, kurt = genextreme.stats(a, moments='mvsk')
            x = np.linspace(genextreme.ppf(0.01, a),
                            genextreme.ppf(0.99, a), 100)
            y = genextreme.pdf(x, a)
            ax.plot(x, y, label="Generalized Extreme Value Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "generalized pareto":
            a = self.param_dic['c']
            b = self.param_dic['scale']
            mean, var, skew, kurt = genpareto.stats(a, moments='mvsk')
            x = np.linspace(genpareto.ppf(0.01, a),
                            genpareto.ppf(0.99, a), 100)
            y = genpareto.pdf(x, a)
            ax.plot(x, y, label="Generalized Pareto Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "geometric":
            a = self.param_dic['p']
            b = self.param_dic['location']
            mean, var, skew, kurt = geom.stats(a, moments='mvsk')
            x = np.arange(geom.ppf(0.01, a),
                          geom.ppf(0.99, a))
            y = geom.pmf(x, a)
            ax.plot(x, y, label="Geometric Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "half normal":
            a = self.param_dic['location']
            b = self.param_dic['scale']
            mean, var, skew, kurt = halfnorm.stats(moments='mvsk')
            x = np.linspace(halfnorm.ppf(0.01),
                            halfnorm.ppf(0.99), 100)
            y = halfnorm.pdf(x)
            ax.plot(x, y, label="Half-normal Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "hypergeometric":
            a = self.param_dic['M']
            b = self.param_dic['n']
            c = self.param_dic['N']
            # There are three parameters for hypergeometric distributions,
            # but we are setting sample size as a constant
            N = c
            rv = hypergeom(a, b, N)
            x = np.arange(0, b + 1)
            y = rv.pmf(x)
            ax.plot(x, y, label="Hypergeometric Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "lognormal":
            a = self.param_dic['sigma']
            b = self.param_dic['scale']
            mean, var, skew, kurt = lognorm.stats(a, moments='mvsk')
            x = np.linspace(lognorm.ppf(0.01, a),
                            lognorm.ppf(0.99, a), 100)
            y = lognorm.pdf(x, a,scale=b)
            ax.plot(x, y, label="Lognormal Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "negative binomial":
            a = self.param_dic['n']
            b = self.param_dic['p']
            mean, var, skew, kurt = nbinom.stats(a, b, moments='mvsk')
            x = np.arange(nbinom.ppf(0.01, a, b),
                          nbinom.ppf(0.99, a, b))
            y = nbinom.pmf(x, a, b)
            ax.plot(x, y, label="Negative Binomial Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "noncentral f":
            a = self.param_dic['dfn']
            b = self.param_dic['dfd']
            x = np.linspace(-1, 8, num=500)
            y = stats.f.cdf(x, a, b)
            ax.plot(x, y, label="Noncentral F Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "noncentral t":
            a = self.param_dic['df']
            b = self.param_dic['nc']
            mean, var, skew, kurt = t_dist.stats(a, moments='mvsk')
            x = np.linspace(nct.ppf(0.01, a, b),
                            nct.ppf(0.99, a, b), 100)
            y = nct.pdf(x, a, nc=b)
            ax.plot(x, y, label="Noncentral t Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "noncentral chi-squared":
            a = self.param_dic['df']
            b = self.param_dic['nc']
            mean, var, skew, kurt = ncx2.stats(a, b, moments='mvsk')
            x = np.linspace(ncx2.ppf(0.01, a, b),
                            ncx2.ppf(0.99, a, b), 100)
            y = ncx2.pdf(x, a, b)
            ax.plot(x, y, label="Noncentral Chi-squared Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "rayleigh":
            a = self.param_dic['scale']
            b = self.param_dic['location']
            mean, var, skew, kurt = rayleigh.stats(moments='mvsk')
            x = np.linspace(rayleigh.ppf(0.01),
                            rayleigh.ppf(0.99), 100)
            y = rayleigh.pdf(x, scale = a, loc = b)
            ax.plot(x, y, label="Rayleigh Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "stable":
            a = self.param_dic['alpha']
            b = self.param_dic['beta']
            mean, var, skew, kurt = levy_stable.stats(a, b, moments='mvsk')
            x = np.linspace(levy_stable.ppf(0.01, a, b),
                            levy_stable.ppf(0.99, a, b), 100)
            y = levy_stable.pdf(x, a, b)
            ax.plot(x, y, label="Stable Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "t":
            a = self.param_dic['df']
            b = self.param_dic['scale']
            mean, var, skew, kurt = t_dist.stats(a, moments='mvsk')
            x = np.linspace(t_dist.ppf(0.01, a),
                            t_dist.ppf(0.99, a), 100)
            y = t_dist.pdf(x, a,scale =b)
            ax.plot(x, y, label="t Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "discrete uniform":
            a = self.param_dic['low']
            b = self.param_dic['high']
            mean, var, skew, kurt = randint.stats(a, b, moments='mvsk')
            x = np.arange(randint.ppf(0.01, a, b),
                          randint.ppf(0.99, a, b))
            y = randint.pmf(x, a, b)
            fig, ax = ax.subplots(1, 1)
            ax.plot(x, y, label="Discrete Uniform Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')
            ax.vlines(x, 0, randint.pmf(x, a, b))

        elif plot == "weibull":
            a = self.param_dic['c']
            b = self.param_dic['scale']
            mean, var, skew, kurt = weibull_min.stats(a, moments='mvsk')
            x = np.linspace(weibull_min.ppf(0.01, a),
                            weibull_min.ppf(0.99, a), 100)
            y = weibull_min.pdf(x, a,scale =b)
            ax.plot(x, y, label="Weibull Distribution", linewidth=4)
            ax.grid(alpha=0.4, linestyle='--')

        else:
            t = np.arange(0, 3, .01)
            ax = fig.add_subplot(111)
            ax.plot(np.sin(2*np.pi*t))

        #configure axex
        ax.set_xlim([float(self.x_from_input.get()), float(self.x_to_input.get())])

        #draw canvas
        canvas = FigureCanvasTkAgg(fig)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(column=0,row=0)

def main():
    root = tk.Tk()
    root.wm_title("Distribution Player")
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)
    root.resizable(False,False)
    root.update_idletasks()
    player = d_player(master=root)
    player.mainloop()
if __name__ == "__main__":
    main()