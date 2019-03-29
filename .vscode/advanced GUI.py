import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import urllib
import json
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt 

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")


#Graph settings used on PageThree
f = Figure()
a = f.add_subplot(111)


#live animation function for graph.
def animate(i):
    dataLink = "https://api.btcmarkets.net/market/BTC/AUD/trades"
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)
    
    data = pd.DataFrame(data)
    
    buys = data
    buys["datestamp"] = np.array(buys["date"]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()

    a.clear()

    a.plot_date(buyDates, buys["price"], "#00A3E0", label="buys")
    a.legend(bbox_to_anchor=(0, 1.20, 1, 0.102), loc=3, 
            ncol=2, borderaxespad=0)
    title = "Bitcoin USD price\nLast Price: "+str(data["price"][499])
    a.set_title(title)
    


    

#define the class
class SeaofBTCapp(tk.Tk):

    #defining the initialization method with room for args and kwargs
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, default="snakeicon.ico")
        tk.Tk.wm_title(self, "NokiaSnake client")

        #defining container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)


        self.frames = {}

        for F in (StartPage, BTCe_page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = """ALPHA Bitcoin trading application
        use at your own risk. There is no promise
        of warranty""", font = "LARGE_FONT")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Agree", 
                            command = lambda: controller.show_frame(BTCe_page))
        button1.pack()

        button2 = ttk.Button(self, text = "Disagree", 
                             command = quit)
        button2.pack()


class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page One", font = "LARGE_FONT")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back to Home", 
                             command = lambda: controller.show_frame(StartPage))
        button1.pack()



class BTCe_page(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Graph Page!", font = "LARGE_FONT")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back to Home", 
                             command = lambda: controller.show_frame(StartPage))
        button1.pack()

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH, expand = True)


#Basic app is set to the class SeaofBTCapp
app = SeaofBTCapp()
app.geometry("1280x720")
#animation function is run for the graph f, with function animate and interval of 1000 millisecs
ani = animation.FuncAnimation(f,  animate, interval = 15000)
app.mainloop()
