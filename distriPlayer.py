# import needed libraries
import tkinter as tk
from tkinter import Checkbutton, ttk
from tkinter.constants import BOTTOM, RIGHT
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import math
import scipy.stats as stats
from scipy.special import factorial

# import specific distributions
from scipy.stats import norm
from scipy.stats import expon
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

# array of all different types of distributions
distributions = ["normal","uniform","poisson","beta","binomial","burr","chi-squared","exponential",
                 "extreme value","f","gamma","generalized extreme value","generalized pareto",
                 "geometric","half normal","hypergeometric","lognormal","negative binomial",
                 "noncentral f","noncentral t","noncentral chi-squared","rayleigh","stable",
                 "t","discrete uniform","weibull"]

# dictionary to retreive parameter dictionary from distribution name
d_to_param = {
"normal":{'mu': 0, 'sigma': 1},
"uniform":{'a': 0, 'b':1},
"poisson":{'lambda':5},
"beta":{'a':2,'b':2},
"binomial":{'n':20,'p':0.5},
"burr":{'c':10,'d':5},
"chi-squared":{'k':4,'location':0},
"exponential":{'location':0,'lambda':1},
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
"discrete uniform":{'low':5,'high':20},
"weibull":{'c':2,'scale':1}
}

# x limit dictionary
d_to_xlim = {
"normal":[-3.5,3.5],
"uniform":[-0.25,1.25],
"poisson":[0,20],
"beta":[0,1],
"binomial":[2,17],
"burr":[0.6,2],
"chi-squared":[0,20],
"exponential":[0,10],
"extreme value":[-6,4],
"f":[0.3,2.8],
"gamma":[0,7],
"generalized extreme value":[-2,7],
"generalized pareto":[0,6],
"geometric":[0,7],
"half normal":[0,3.5],
"hypergeometric":[0,10],
"lognormal":[0,10],
"negative binomial":[-2,20],
"noncentral f":[-1,9],
"noncentral t":[-2,6],
"noncentral chi-squared":[0,45],
"rayleigh":[0,3.5],
"stable":[-5,5],
"t":[-5,5],
"discrete uniform":[4,21],
"weibull":[0,2.5]
}

class d_player(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    
    def get_dist(self,event):
        # get selected value
        self.dist_cb.get()

        # remove old parameter labels
        for label in self.param_label:
            self.param_label[label].grid_remove()

        # remove old entries
        for entry in self.param_entry:
            self.param_entry[entry].grid_remove()

        # set dictionary of parameters
        self.param_dic = d_to_param[self.dist_cb.get()]

        # update parameters gui
        self.param_entry = {}
        self.param_label = {}
        for i, lab in enumerate(self.param_dic):
            self.param_label[lab] = tk.Label(text=lab)
            self.param_label[lab].grid(column=2 * i + 2, row=4)
            self.param_entry[lab] = tk.Entry(width=3)
            self.param_entry[lab].insert(0, self.param_dic[lab])
            self.param_entry[lab].grid(column=2 * i + 3, row=4)
        
        # set distionary for x range
        self.x_range = d_to_xlim[self.dist_cb.get()]

        # update parameters gui
        self.x_from = tk.Label(text="from")
        self.x_from.grid(column=2,row=3)
        self.x_from_input = tk.Entry(width=3)
        self.x_from_input.insert(0, self.x_range[0])
        self.x_from_input.grid(column=3, row=3)

        self.x_to = tk.Label(text="to")
        self.x_to.grid(column=4, row=3)
        self.x_to_input = tk.Entry(width=3)
        self.x_to_input.insert(0, self.x_range[1])
        self.x_to_input.grid(column=5, row=3)

        # set x range values
        self.x_from_input.delete(0, 'end')
        self.x_from_input.insert(0, d_to_xlim[self.dist_cb.get()][0])
        self.x_to_input.delete(0, 'end')
        self.x_to_input.insert(0, d_to_xlim[self.dist_cb.get()][1])


        # creat plot button
        self.plot_button = tk.Button(text="Plot!", width=10)
        self.plot_button.grid(column=1, row=6)
        self.plot_button["command"] = lambda plot=self.dist_cb.get(): self.switch_plot(plot)

        return self.dist_cb.get()

    def create_widgets(self):

        # distribution combobox
        self.dist = tk.Label(text="distribution")
        self.dist.grid(column=0,row=0)

        self.selected_dist = tk.StringVar()
        self.dist_cb = ttk.Combobox(textvariable=self.selected_dist, width=20)
        self.dist_cb['values'] = distributions
        self.dist_cb['state'] = 'readonly'

        self.dist_cb.bind('<<ComboboxSelected>>', self.get_dist)
        self.dist_cb.grid(column=1,row=0)

        # x range
        self.x_range = tk.Label(text="x")
        self.x_range.grid(column=1,row=3)
        self.x_range = []

        # parameters
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

        # update dictionary from click
        for lab in self.param_dic:
            self.param_dic[lab] = float(self.param_entry[lab].get())


        # update x range from click
        self.x_range[0] = float(self.x_from_input.get())
        self.x_range[1] = float(self.x_to_input.get())

        # check if invalid x range
        if self.x_range[0] > self.x_range[1]:
            tk.messagebox.showwarning(title="ERROR", message="Please input a valid x range")
            return

        # x range
        x = np.linspace(self.x_range[0], self.x_range[1], 100)

        # linewidth
        lw = 4

        if plot == "normal":
            a = self.param_dic['mu']
            sigma = self.param_dic['sigma']
            y = norm.pdf(x, a, sigma)
            ax.plot(x, y, label="Normal Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "uniform":
            a = self.param_dic['a']
            b = self.param_dic['b']
            y = 1/(b-a)
            ax.hlines(y, xmin=a, xmax=b, linewidth=lw)
            ax.hlines(0, xmin=self.x_range[0], xmax=a, linewidth=lw)
            ax.hlines(0, xmin=b, xmax=self.x_range[1], linewidth=lw)
            ax.vlines(a, ymin=0, ymax=y, linewidth=lw)
            ax.vlines(b, ymin=0, ymax=y, linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "poisson":
            a = self.param_dic['lambda']
            y = np.exp(-a) * np.power(a, x) / factorial(x)
            ax.plot(x, y, label="Poisson Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "beta":
            a = self.param_dic['a']
            b = self.param_dic['b']
            y = beta.pdf(x, a, b, scale=1, loc=0)
            ax.plot(x, y, label="Beta Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "binomial":
            a = self.param_dic['n']
            b = self.param_dic['p']
            x = np.arange(self.x_range[0], self.x_range[1])
            y = binom.pmf(x, a, b)
            ax.plot(x, y, label="Binomial Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "burr":
            a = self.param_dic['c']
            b = self.param_dic['d']
            y = burr.pdf(x, a, b)
            ax.plot(x, y, label="Burr Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "chi-squared":
            a = self.param_dic['k']
            y = chi2.pdf(x, df=a)
            ax.plot(x, y, label="Chi-squared distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "exponential":
            a = self.param_dic['location']
            b = self.param_dic['lambda']
            y = expon.pdf(x, a, b)
            ax.plot(x, y, label="Exponential Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "extreme value":
            a = self.param_dic['location']
            b = self.param_dic['scale']
            y = gumbel_l.pdf(x)
            ax.plot(x, y, label="Extreme Value Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "f":
            a = self.param_dic['v1']
            b = self.param_dic['v2']
            y = f.pdf(x, a, b)
            ax.plot(x, y, label="F Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "gamma":
            a = self.param_dic['k']
            b = self.param_dic['theta']
            y = gamma.pdf(x, a)
            ax.plot(x, y, label="Gamma Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "generalized extreme value":
            a = self.param_dic['c']
            b = self.param_dic['scale']
            y = genextreme.pdf(x, a)
            ax.plot(x, y, label="Generalized Extreme Value Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "generalized pareto":
            a = self.param_dic['c']
            b = self.param_dic['scale']
            y = genpareto.pdf(x, a)
            ax.plot(x, y, label="Generalized Pareto Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "geometric":
            a = self.param_dic['p']
            b = self.param_dic['location']
            x = np.arange(self.x_range[0], self.x_range[1])
            y = geom.pmf(x, a)
            ax.plot(x, y, label="Geometric Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "half normal":
            a = self.param_dic['location']
            b = self.param_dic['scale']
            y = halfnorm.pdf(x)
            ax.plot(x, y, label="Half-normal Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "hypergeometric":
            a = self.param_dic['M']
            b = self.param_dic['n']
            c = self.param_dic['N']
            # There are three parameters for hypergeometric distributions,
            # but we are setting sample size as a constant
            N = c
            rv = hypergeom(a, b, N)
            x = np.arange(self.x_range[0], self.x_range[1])
            y = rv.pmf(x)
            ax.plot(x, y, label="Hypergeometric Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "lognormal":
            a = self.param_dic['sigma']
            b = self.param_dic['scale']
            y = lognorm.pdf(x, a,scale=b)
            ax.plot(x, y, label="Lognormal Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "negative binomial":
            a = self.param_dic['n']
            b = self.param_dic['p']
            x = np.arange(self.x_range[0], self.x_range[1])
            y = nbinom.pmf(x, a, b)
            ax.plot(x, y, label="Negative Binomial Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "noncentral f":
            a = self.param_dic['dfn']
            b = self.param_dic['dfd']
            y = f.pdf(x, a, b)
            ax.plot(x, y, label="Noncentral F Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "noncentral t":
            a = self.param_dic['df']
            b = self.param_dic['nc']
            y = nct.pdf(x, a, nc=b)
            ax.plot(x, y, label="Noncentral t Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "noncentral chi-squared":
            a = self.param_dic['df']
            b = self.param_dic['nc']
            y = ncx2.pdf(x, a, b)
            ax.plot(x, y, label="Noncentral Chi-squared Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "rayleigh":
            a = self.param_dic['scale']
            b = self.param_dic['location']
            y = rayleigh.pdf(x, scale = a, loc = b)
            ax.plot(x, y, label="Rayleigh Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "stable":
            a = self.param_dic['alpha']
            b = self.param_dic['beta']
            y = levy_stable.pdf(x, a, b)
            ax.plot(x, y, label="Stable Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "t":
            a = self.param_dic['df']
            b = self.param_dic['scale']
            y = t_dist.pdf(x, a,scale =b)
            ax.plot(x, y, label="t Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        elif plot == "discrete uniform":
            a = self.param_dic['low']
            b = self.param_dic['high']
            x = np.arange(self.x_range[0], self.x_range[1])
            y = randint.pmf(x, a, b)
            ax.plot(x, y, label="Discrete Uniform Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')
            ax.vlines(x, 0, randint.pmf(x, a, b), linestyle='--', linewidth=0.25 * lw)

        elif plot == "weibull":
            a = self.param_dic['c']
            b = self.param_dic['scale']
            y = weibull_min.pdf(x, a,scale =b)
            ax.plot(x, y, label="Weibull Distribution", linewidth=lw)
            ax.grid(alpha=0.4, linestyle='--')

        else:
            y = np.sin(2*np.pi*x)
            ax.plot(x,y)

        # configure log-scale
        if self.is_log_check_var.get() == 1:
            ax.set_yscale('log')
        
        # configure axex
        ax.set_xlim([float(self.x_from_input.get()), float(self.x_to_input.get())])

        # draw canvas
        canvas = FigureCanvasTkAgg(fig)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(column=0,row=7)

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
