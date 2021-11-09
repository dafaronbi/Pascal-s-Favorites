import tkinter as tk
from tkinter import Checkbutton, ttk
import numpy as np
import scipy.stats as stats
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

distributions = ["normal","uniform","poison","beta","binomial","burr","chi-squared","exponential",
                 "extreme value","f","gamma","generalized extreme value","generalized pareto",
                 "geometric","half normal","hypergeometric","lognormal","negative binomial",
                 "noncentral f","noncentral t","noncentral chi-squared","rayleigh","stable",
                 "t","discret uniform","weibull"]

# TODO
# add param names for each distribution
# add default param values
# add default x range

window = tk.Tk()
window.geometry('1280x768')
window.title("Distribution Plotter")

# for later change to variable size
width = 1280
height = 768
a = "a = "
b = "b = "
# plot number of steps
steps = 1000

##################################################
# functions
##################################################

# TODO: test purpose, delete later
def choose_dist(event):
    msg = f"selected {dist_cb.get()}"
    tk.messagebox.showinfo(title = "test", message = msg)

# TODO
def plot(dist):
    fig = Figure(figsize=(5, 4), dpi=100)
    # plot the appropriate distribution
    if dist == 'normal':
        mu = 0
        variance = 1
        sigma = variance ** (1/2)
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)
        fig.add_subplot(111).plot(y)
    elif dist == 'uniform':
        y = np.full(100,0.01)
        fig.add_subplot(111).plot(y)

class Distribution:
    def __init__(self, name, params, x_range, is_log):
        self.name = name
        self.params = params
        self.x_range = x_range
        self.is_log = is_log

##################################################
# label and user input
##################################################

# distribution combobox
dist = tk.Label(text = "distribution")
dist.place(relx = 0.70, rely = 0.25, anchor = 'nw')

selected_dist = tk.StringVar()
dist_cb = ttk.Combobox(window, textvariable = selected_dist, width = 20)
dist_cb['values'] = distributions
dist_cb['state'] = 'readonly'
dist_cb.place(relx = 0.80, rely = 0.25, anchor = 'nw')

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

param_a = tk.Label(text = a)
param_a.place(relx = 0.80, rely = 0.45, anchor = 'nw')
param_a_input = tk.Entry(width = 3)
param_a_input.place(relx = 0.85, rely = 0.45, anchor = 'nw')

param_b = tk.Label(text = b)
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

# TODO: test purpose, delete later
dist_cb.bind('<<ComboboxSelected>>', choose_dist)

def plot(dist):
    fig = Figure(figsize = (5, 4), dpi = 100)
    ax = fig.add_subplot(111)
    # plot the appropriate distribution
    if dist == 'normal':
        mu = 0
        variance = 1
        sigma = variance ** (1/2)
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        y = stats.norm.pdf(x, mu, sigma)
        fig.add_subplot(111).plot(y)
    elif dist == 'uniform':
        y = np.full(100,0.01)
        fig.add_subplot(111).plot(y)
    
    ax.set_title (dist, fontsize = 16)
    ax.set_ylabel("Y", fontsize = 14)
    ax.set_xlabel("X", fontsize = 14)

    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().place(relx = 0.35, rely = 0.5, anchor = 'center')
    canvas.draw()

plot(dist_cb.get())

window.mainloop()
