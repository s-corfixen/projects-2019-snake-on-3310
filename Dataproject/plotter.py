import tkinter as tk
from tkinter import ttk
import pandas as pd 
import numpy as np 

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pydst



class DataPlotter:
    
    def __init__(self,figure):
        
        self.fig = figure
        self.subplots = {}
    
    def addlineplot(self,data,plotname, color="r"):
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.plot(data[xaxisname],data[yaxisname],color=color)
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)
        self.subplots[plotname]=currentplot
        
    def addtwinxlineplot(self, data, plotname,color="b"):
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        currentplot = self.subplots[plotname].twinx()
        currentplot.plot(data[xaxisname],data[yaxisname],color=color)
        currentplot.set_ylabel(yaxisname)
        self.subplots[plotname+"twinx"]=currentplot

    def addbarplot(self,data,plotname, color="g"):
        axiskeys = data.keys()
        xaxisname = axiskeys[0]
        yaxisname = axiskeys[1]
        currentplot = self.fig.add_subplot(1,1,1)
        currentplot.bar(data[xaxisname],data[yaxisname],color=color)
        currentplot.set_xlabel(xaxisname)
        currentplot.set_ylabel(yaxisname)
        self.subplots[plotname]=currentplot
    
    def figuretitle(self, figuretitle):
        self.fig.suptitle(figuretitle)

    def clearplots(self):
        self.fig.clear()
        self.subplots.clear()



class PlotterWindow:
    def __init__(self,xsize, ysize, data):

        self.xsize = xsize
        self.ysize = ysize
        self.data = data

        self.window = tk.Tk()

        self.currentslicekey = tk.StringVar()

        self.slicekeys = sorted(self.data["Municipality"].unique())

        self.graphmenu = tk.OptionMenu(self.window, self.currentslicekey, *self.slicekeys, command = lambda x: self.ongraphmenuchange())
        self.graphmenu.pack()

        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)

        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand = True)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH, expand = True)
        
        self.window.geometry(str(self.xsize) + "x" + str(self.ysize))

        self.plotter = DataPlotter(self.figure)

    def start(self):
        self.window.mainloop()
    
    def ongraphmenuchange(self):
        self.updateplotter(self.currentslicekey.get())
        self.canvas.draw()

    def updateplotter(self, graphnamekey):
        self.plotter.clearplots()
        self.plotter.figuretitle(graphnamekey)
        newplotdata = self.data.loc[self.data["Municipality"] == graphnamekey,:]

        self.plotter.addbarplot(newplotdata[["Year","Surplus"]],"plot1")
        self.plotter.addtwinxlineplot(newplotdata[["Year","People"]],"plot1")


    #graphs = sorted(data[graphnames].unique())

    
    



# if __name__ == "__main__":

#     window = PlotterWindow(1280,720)
#     window.start()






#     data1 = pd.DataFrame({"diller":[1,2,3],  "z":[2,5,8], "dreng":[4,7,3]})    
#     data2 = pd.DataFrame({"x":[1,2,3], "y":[3,1,9]}) 

#     print(data1[["z","dreng"]])
#     window = tk.Tk()
#     def open_window(xsize,ysize):
#        figure = Figure()
#        canvas = FigureCanvasTkAgg(figure, window)
#        toolbar = NavigationToolbar2Tk(canvas, window)
        
     #   graph = DataPlotter(figure)
        #graph.addlineplot(data1[["dreng","z"]],"hobbit")
        #graph.addtwinxlineplot(data2,"hobbit")
      #  graph.figuretitle("Perle")
        
       # canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand = True)
        #toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH, expand = True)

        #button = tk.Button(window, text = "Clear", command = lambda: buttonclick(canvas,graph))
        #button.pack()
        #window.geometry(str(xsize) + "x" + str(ysize))
        #canvas.draw()
        
    
    #open_window(1280,720)
    #window.mainloop()