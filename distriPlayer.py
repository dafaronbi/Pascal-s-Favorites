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
from scipy.stats import t
from scipy.stats import ncx2
from scipy.stats import rayleigh
from scipy.stats import levy_stable
from scipy.stats import randint
from scipy.stats import weibull_min


#Array of all different types of distributions
distributions = ["normal","uniform","poison","beta","binomial","burr","chi-squared","exponential",
                 "extreme value","f","gamma","generalized extreme value","generalized pareto",
                 "geometric","half normal","hypergeometric","lognormal","negative binomial",
                 "noncentral f","noncentral t","noncentral chi-squared","rayleigh","stable",
                 "t","discret uniform","weibull"]

ab = [(0, 1), (0, 1), (5, None), (2, 2), (20, 0.5), (10, 5), (4, None), (1, 1), 
      (None, None), (30, 20), (2, None), (-0.1, None), (0.1, None), 
      (0.5, None), (None, None), (20, 7), (0.95, None), (5, 0.5), 
      (3, 2), (3, None), (20, 1), (None, None), (2, -0.5), 
      (3, None), (5, 20), (2, None)]

xrange = [(-3.5, 3.5), (-1, 2), (0, 20), (-60, 60), (2, 18), (0.8, 2), (0, 20), (0, 10), 
          (-5, 2), (0, 3), (0, 7), (-2, 6), (0, 6), 
          (0, 7), (0, 3), (0, 8), (0, 10), (0, 14), 
          (-1, 9), (-5, 5), (7, 42), (0, 3.5), (-4, 4), 
          (-5, 5), (4, 19), (0, 2)]

class d_player(tk.Frame):
    selected = ""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.cb_input = ""

    def create_widgets(self):
        #cb_input = ""
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

        # def dist_changed(event):
        #     return dist_cb.get()

        def get_dist(event):
            self.selected = dist_cb.get()
            print(dist_cb.get())

            # plot button
            plot_button = tk.Button(text = "Plot!", width = 10)
            plot_button.place(relx = 0.80, rely = 0.65, anchor = 'nw')
            #cb_input = dist_cb.get()
            #dist_cb.bind('<<ComboboxSelected>>', self.switch_plot)
            plot_button["command"] = lambda plot=dist_cb.get(): self.switch_plot(plot)
            #self.switch_plot(dist_cb.get())
            #cb_input = dist_cb.get()
            return dist_cb.get()

        selected_dist = tk.StringVar()
        dist_cb = ttk.Combobox(frame, textvariable = selected_dist, width = 20)
        dist_cb['values'] = distributions
        dist_cb['state'] = 'readonly'
        #dist_cb.current(1)
        cb_input = dist_cb.bind('<<ComboboxSelected>>', get_dist)
        print(cb_input)
        # dist_cb.bind('<<ComboboxSelected>>', lambda _ : print("plot!"))
        dist_cb.pack(pady=300)
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
        #plot_button = tk.Button(text = "Plot!", width = 10)
        #plot_button.place(relx = 0.80, rely = 0.65, anchor = 'nw')
        #cb_input = dist_cb.get()
        #dist_cb.bind('<<ComboboxSelected>>', self.switch_plot)
        #plot_button["command"] = lambda plot=cb_input: self.switch_plot(plot)

        # self.switch_plot(cb_input)

        #self.quit = tk.Button(self.sideBar, text="QUIT", fg="red", command=self.master.destroy,)
        #self.quit.pack(side="bottom", fill=tk.X)


    def switch_plot(self, plot):

        for widget in self.mainView.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.mainView)

        # add canvas for mat plot
        fig = Figure(figsize=(5, 4), dpi=100)

        index = distributions.index(plot)
        a = ab[index][0]
        b = ab[index][1]
        xmin = xrange[index][0]
        xmax = xrange[index][1]

        self.distribution(plot, fig, a, b, xmin, xmax)
        # #plot the apropriate distribution
        # if plot == "normal":
        #     mu = 0
        #     variance = 1
        #     sigma = math.sqrt(variance)
        #     x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        #     y = stats.norm.pdf(x, mu, sigma)
        #     fig.add_subplot(111).plot(y)

        # elif plot == "uniform":
        #     y = np.full(100,0.01)
        #     fig.add_subplot(111).plot(y)

        # elif plot == "poison":
        #     t = np.arange(0, 3, .01)
        #     y = np.exp(-5)*np.power(5, t)/factorial(t)
        #     fig.add_subplot(111).plot(y)

        # elif plot == "t":
        #     mu = 0
        #     variance = 1
        #     sigma = math.sqrt(variance)
        #     df = 2.74
        #     x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        #     y = stats.t.pdf(x, df)
        #     fig.add_subplot(111).plot(y)

        # elif plot == "beta":
        #     mu = 0
        #     variance = 1
        #     sigma = math.sqrt(variance)
        #     x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        #     a = 2
        #     b = 2
        #     y = stats.beta.pdf(x,a,b, scale=100, loc=-50)
        #     fig.add_subplot(111).plot(y)
        # else:
        #     t = np.arange(0, 3, .01)
        #     fig.add_subplot(111).plot(np.sin(2*np.pi*t))

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand=1)

        frame.pack(fill=tk.BOTH)
        # frame.grid(row=0, column=0, sticky="nsew")
    

    def distribution(self, plot, fig, a, b, xmin, xmax):
        if plot == "normal":
            #a: mu = 0
            #b: variance = 1
            #xrange: [-3.5, 3.5]
            sigma = math.sqrt(b)
            x = np.linspace(a - 3*sigma, a + 3*sigma, 100)
            y = stats.norm.pdf(x, a, sigma)
            # plt.plot(x, y, label = "Normal Distribution", linewidth = 4)
            # plt.grid(alpha = 0.4, linestyle = '--')
            # plt.xlim([xmin, xmax])
            ax = fig.add_subplot(111)
            ax.plot(x, y)
            ax.title.set_text("Normal Distribution")
            ax.legend([r"$\mu$" + "=" + str(a) + "\n" +  r"$\sigma$" + "=" + str(b)], 
                      loc='best', handlelength=0)
            #ax.legend([r"$\sigma$"], loc=4)
            #ax.annotate(["mu", "sigma"], xy=(0,0))

            
        elif plot == "uniform":
            #a = 0
            #b = 1
            #xrange: [-1, 2]
            y = 1
            x = np.arange(0, 1)
            plt.hlines(y, xmin = 0, xmax = 1, linewidth = 4)
            plt.hlines(0, xmin = -.5, xmax = a, linewidth = 4)
            plt.hlines(0, xmin = b, xmax = 1.5, linewidth = 4)
            plt.vlines(a, ymin = 0, ymax = y, linewidth = 4)
            plt.vlines(b, ymin = 0, ymax = y, linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])

        elif plot == "poisson":
            #a: mu = 5
            #b: n/a
            #xrange: [0, 20]
            x = np.arange(0, 20, 0.1)
            y = np.exp(-a)*np.power(a, x)/factorial(x)
            plt.plot(x, y, label = "Poisson Distribution", linewidth = 5)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "beta":
            #a: alpha = 2
            #b: beta = 2
            #xrange: [-60, 60]
            x = np.arange (-50, 50, 0.1)
            y = beta.pdf(x, a, b, scale=100, loc=-50)
            plt.plot(x, y, label = "Beta Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])  
            
        elif plot == "binomial":
            #a: n = 20
            #b: p = 0.5
            #xrange: [2, 18]
            x = np.arange(binom.ppf(0.001, a, b),
                binom.ppf(0.999, a, b))
            y = binom.pmf(x, a, b)
            plt.plot(x, y, label = "Binomial Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])  
            
        elif plot == "burr":
            #a: c = 10
            #b: d = 5
            #xrange: [0.8, 2]
            x = np.linspace(burr.ppf(0.01, a, b),
                    burr.ppf(0.99, a, b), 100)
            y = burr.pdf(x, a, b)
            plt.plot(x, y, label = "Burr Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])  
            
        elif plot == "chi-squared":
            #a: k (degrees of freedom) = 4
            #b: N/A
            #xrange: [0, 20]
            x = np.arange(0, 20, 0.001)
            y = chi2.pdf(x, df = a)
            plt.plot(x, y, label = "Chi-squared distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax]) 

        elif plot == "exponential":
            #a: mu = 1
            #b: sigma = 1
            #xrange: [0, 10]
            x = np.arange(0, 20, 0.001)
            y = ss.expon.pdf(x, a, b)
            plt.plot(x, y, label = "Exponential Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "extreme value":
            #a: ???
            #b: ???
            #xrange: [-5, 2]
            mean, var, skew, kurt = gumbel_l.stats(moments='mvsk')
            x = np.linspace(gumbel_l.ppf(0.01),
                    gumbel_l.ppf(0.99), 100)        
            y = gumbel_l.pdf(x)
            plt.plot(x, y, label = "Extreme Value Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "f":
            #a: v1 = 30
            #b: v2 = 20
            #xrange: [0, 3]
            mean, var, skew, kurt = f.stats(a, b, moments='mvsk')
            x = np.linspace(f.ppf(0.01, a, b),
                            f.ppf(0.99, a, b), 100)
            y = f.pdf(x, a, b)
            plt.plot(x, y, label = "F Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "gamma":
            #a: k = 2
            #b: ??? (shouldn't there be two?)
            #xrange: [0, 7]
            mean, var, skew, kurt = gamma.stats(a, moments='mvsk')
            x = np.linspace(gamma.ppf(0.01, a),
                            gamma.ppf(0.99, a), 100)
            y = gamma.pdf(x, a)
            plt.plot(x, y, label = "Gamma Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "generalized extreme value":
            #a: c = -0.1
            #b: ???
            #xrange: [-2, 6]
            mean, var, skew, kurt = genextreme.stats(a, moments='mvsk')
            x = np.linspace(genextreme.ppf(0.01, a),
                            genextreme.ppf(0.99, a), 100)
            y = genextreme.pdf(x, a)
            plt.plot(x, y, label = "Generalized Extreme Value Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "generalized pareto":
            #a: c = 0.1
            #b: ???
            #xrange: [0, 6]
            mean, var, skew, kurt = genpareto.stats(a, moments='mvsk')
            x = np.linspace(genpareto.ppf(0.01, a),
                            genpareto.ppf(0.99, a), 100)
            y = genpareto.pdf(x, a)
            plt.plot(x, y, label = "Generalized Pareto Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])

        elif plot == "geometric":
            #a: p = 0.5
            #b: ???
            #xrange: [0, 7]
            mean, var, skew, kurt = geom.stats(a, moments='mvsk')
            x = np.arange(geom.ppf(0.01, a),
                        geom.ppf(0.99, a))
            y = geom.pmf(x, a)
            plt.plot(x, y, label = "Geometric Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "half normal":
            #a: ??? No paremeters ???
            #b: ???
            #xrange: [0, 3]
            mean, var, skew, kurt = halfnorm.stats(moments='mvsk')
            x = np.linspace(halfnorm.ppf(0.01),
                            halfnorm.ppf(0.99), 100)
            y = halfnorm.pdf(x)
            plt.plot(x, y, label = "Half-normal Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "hypergeometric":
            #a: M = 20
            #b: n = 7
            #c: N = 15
            #There are three parameters for hypergeometric distributions,
            #but we are setting sample size as a constant (15)
            #xrange: [0, 8]
            N = 15
            rv = hypergeom(a, b, N)
            x = np.arange(0, b+1)
            y = rv.pmf(x)
            plt.plot(x, y, label = "Hypergeometric Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])

        elif plot == "lognormal":
            #a: s = 0.95
            #b: ???
            #xrange: [0, 10]
            mean, var, skew, kurt = lognorm.stats(a, moments='mvsk')
            x = np.linspace(lognorm.ppf(0.01, a),
                            lognorm.ppf(0.99, a), 100)
            y = lognorm.pdf(x, a)
            plt.plot(x, y, label = "Lognormal Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])

        elif plot == "negative binomial":
            #a: n = 5
            #b: p = 0.5
            #xrange: [0, 14]
            mean, var, skew, kurt = nbinom.stats(a, b, moments='mvsk')
            x = np.arange(nbinom.ppf(0.01, a, b),
                        nbinom.ppf(0.99, a, b))
            y = nbinom.pmf(x, a, b)
            plt.plot(x, y, label = "Negative Binomial Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "noncentral f":
            #a: dfn = 3
            #b: dfd = 2
            #xrange: [-1, 9]
            x = np.linspace(-1, 8, num = 500)
            y = stats.f.cdf(x, a, b)
            plt.plot(x, y, label = "Noncentral F Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "noncentral t":
            #a: df = 3
            #b: ???
            #xrange: [-5, 5]
            mean, var, skew, kurt = t.stats(a, moments='mvsk')
            x = np.linspace(t.ppf(0.01, a),
                            t.ppf(0.99, a), 100)
            y = t.pdf(x, a)
            plt.plot(x, y, label = "Noncentral t Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])

        elif plot == "noncentral chi-squared":
            #a: df = 20
            #b: nc = 1
            #xrange: [7, 42]
            mean, var, skew, kurt = ncx2.stats(a, b, moments='mvsk')
            x = np.linspace(ncx2.ppf(0.01, a, b),
                            ncx2.ppf(0.99, a, b), 100)
            y = ncx2.pdf(x, a, b)
            plt.plot(x, y, label = "Noncentral Chi-squared Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "rayleigh":
            #a: ??? No parameters ???
            #b: ???
            #xrange: [0, 3.5]
            mean, var, skew, kurt = rayleigh.stats(moments='mvsk')
            x = np.linspace(rayleigh.ppf(0.01),
                            rayleigh.ppf(0.99), 100)
            y = rayleigh.pdf(x)
            plt.plot(x, y, label = "Rayleigh Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])
            
        elif plot == "stable":
            #a: alpha = 2
            #b: beta = -0.5
            #xrange: [-4, 4]
            mean, var, skew, kurt = levy_stable.stats(a, b, moments='mvsk')
            x = np.linspace(levy_stable.ppf(0.01, a, b),
                            levy_stable.ppf(0.99, a, b), 100)
            y = levy_stable.pdf(x, a, b)
            plt.plot(x, y, label = "Stable Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])        

        elif plot == "t":
            #a: df = 3
            #b: ???
            #xrange: [-5, 5]
            mean, var, skew, kurt = t.stats(a, moments='mvsk')
            x = np.linspace(t.ppf(0.01, a),
                            t.ppf(0.99, a), 100)
            y = t.pdf(x, a)
            plt.plot(x, y, label = "t Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax])  
            
        elif plot == "discrete uniform":
            #a: low = 5
            #b: high = 20
            #xrange: [4, 19]
            mean, var, skew, kurt = randint.stats(a, b, moments='mvsk')
            x = np.arange(randint.ppf(0.01, a, b),
                        randint.ppf(0.99, a, b))
            y = randint.pmf(x, a, b)
            fig, ax = plt.subplots(1, 1)
            plt.plot(x, y, label = "Discrete Uniform Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            ax.vlines(x, 0, randint.pmf(x, a, b))
            plt.xlim([xmin, xmax]) 
            
        elif plot == "weibull":
            #a: c = 2
            #b: ???
            #xrange: [0, 2]
            mean, var, skew, kurt = weibull_min.stats(a, moments='mvsk')
            x = np.linspace(weibull_min.ppf(0.01, a),
                            weibull_min.ppf(0.99, a), 100)
            y = weibull_min.pdf(x, a)
            plt.plot(x, y, label = "Weibull Distribution", linewidth = 4)
            plt.grid(alpha = 0.4, linestyle = '--')
            plt.xlim([xmin, xmax]) 

def main():
    root = tk.Tk()
    root.wm_title("Distribution Player")
    root.geometry("1280x768")
    
    player = d_player(master=root)
    player.mainloop()

if __name__ == "__main__":
    main()
