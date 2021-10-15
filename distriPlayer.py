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