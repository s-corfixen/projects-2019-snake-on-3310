import tkinter as tk
from tkinter import ttk
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt

from pandas_datareader import wb
import pydst

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana",10)
SMALL_FONT = ("Verdana",6)

class NokiaSnakeClient(tk.Tk):

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

        self.frames = {}

        for F in (PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(PageOne)

    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Choosing Dataset", font = "LARGE_FONT")
        label.pack(pady=10,padx=10)

        #defining navigation button
        button1 = ttk.Button(self, text = "Next Page", 
                             command = lambda: controller.show_frame(PageTwo))
        button1.place(x=1180,y=680)

        #Dataset list
        var1 = tk.IntVar()
        var1.set(1)
        
        #Making the list
        datasets = ("example 1"), ("To be added"), ("Custom data")
        tk.Label(self, text="Choose Dataset to be used", justify = tk.LEFT, padx = 20).place(x=550, y=180)

        def LoadDataset():
            if var1.get()==0:
                pd.read_csv("example data.csv")
            elif var1.get()==1:
                pd.read_csv("example data2.csv")
            else:
                popupmsg("Function not supported yet")

        for val, dataset in enumerate(datasets):
            tk.Radiobutton(self, 
                text=dataset,
                variable=var1, 
                command = LoadDataset,
                value=val).place(x=600, y=200+val*20)
        
        
                
        def popupmsg(msg):
            popup = tk.Tk()

            popup.wm_title("!")
            label = ttk.Label(popup, text=msg, font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)

            entrytext = tk.Entry(popup)
            entrytext.pack()

            B1 = ttk.Button(popup, text="Okay", command = savedataset)
            B1.pack()

            def savedataset():
                data = pydst.Dst(lang="en")

            popup.mainloop()        

        



class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Customize Dataset", font = "LARGE_FONT")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back", 
                             command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)

        button2 = ttk.Button(self, text = "Next Page", 
                             command = lambda: controller.show_frame(PageThree))
        button2.place(x=1180,y=680)

        
        #scrollable list
        checkboxlist1 = ScrollableFrame(self)
        checkboxlist1.place(x=50,y=100)

        def button_callback():
          for key, value in Dict1:
              ttk.Checkbutton(checkboxlist1.interior, text=key).grid(row=x, column=0)

        checkbox = ttk.Button(checkboxlist1.interior, text="Update", command=button_callback)
        checkbox.grid(row=0, column=0)

class PageThree(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Statistics and Graphs", font = "LARGE_FONT")
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back", 
                             command = lambda: controller.show_frame(PageTwo))
        button1.place(x=20, y=680)
        
        button2 = ttk.Button(self, text = "Reset")
        button2.place(x=1180,y=680)

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y",  expand="false")
        self.canvas = tk.Canvas(self, bd=0,
                                height=300, width=150,
                                yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        #self.canvas.xview_moveto(0)
        #self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        self.bind("<Configure>", self.set_scrollregion)


    def set_scrollregion(self, event=None):
        """ Set the scroll region on the canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


#if __name__ == "__main__":
#    root = tk.Tk()
    
#Basic app is set to the class NokiaSnakeclient
app = NokiaSnakeClient()
app.geometry("1280x720")
app.mainloop()