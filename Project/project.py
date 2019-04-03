import tkinter as tk
from tkinter import ttk
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
import pydst
from matplotlib import style

Dst = pydst.Dst(lang='da')

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana",10)
SMALL_FONT = ("Verdana",8)

dict1 = {}
dict2 = {}
tableid = "failure"

class NokiaSnakeClient(tk.Tk):

    #defining the initialization method with room for args and kwargs
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, "Project/snakeicon.ico")
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
        label = tk.Label(self, text = "Choosing Dataset", font = LARGE_FONT)
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
                popupmsg()

        for val, dataset in enumerate(datasets):
            tk.Radiobutton(self, 
                text=dataset,
                variable=var1, 
                command = LoadDataset,
                value=val).place(x=600, y=200+val*20)
        
        
                
        def popupmsg():
            popup = tk.Tk()

            popup.wm_title("Load dataset")
            label = ttk.Label(popup, text="BETA feature", font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)       

            entry1 = tk.Entry(popup)
            entry1.pack()

            
            def ok():               
                global tableid
                tableid = entry1.get()
                data = Dst.get_variables(table_id=tableid)
                text = list(data["text"])
                
                for i in text:
                    dataframe = data.loc[data["text"] == i,"values"]
                    data_list = list(dataframe)
                    i_list = []
                    for sublist in data_list:
                        for item in sublist:
                            i_list.append(item)
                    dict1.update({i: i_list})
                for i in text:
                    idapi = data.loc[data["text"]== i, "id"].item()
                    dict2.update({i: idapi})
                
                popup.destroy()

            button = tk.Button(popup, text="Load", command = ok)
            button.pack()

            popup.mainloop()        



class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Customize Dataset", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back", 
                             command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)
        
        def nextpage():
            controller.show_frame(PageThree)
            selectedvariables = {}
            
            for header, elist in dict1.items():
                
                list1 = []
                for key in selected:
                    if selected[key].get()==True:
                        list1.append(key)
                list2 = []
                for dic in elist:
                    if dic["text"] in list1:
                        list2.append(dic["id"])
                if list2 != []:
                    selectedvariables.update({str(dict2[header]): list2})        
            
            savepath = "C:/Users/Corfixen/Documents/projects-2019-snake-on-3310/"+str(tableid)+".csv"
            Dst.get_csv(path = savepath, table_id=tableid, variables = selectedvariables)
            #DATA.to_excel(savepath, sheet_name='Sheet1')
        button2 = ttk.Button(self, text = "Next Page", 
                             command = nextpage)
        button2.place(x=1180,y=680)
        
        selected = {}
        #scrollable list
        def generate():
            for index, key in enumerate(dict1):
                if index > 3:
                    label = tk.Label(self, text = key, font = SMALL_FONT)
                    label.place(x=50+290*(index-4), y=360)
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*(index-4), y=380)

                    for index, value in enumerate(dict1[key]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selected[value["text"]] = is_selected

                else:
                    label = tk.Label(self, text = key, font = SMALL_FONT)
                    label.place(x=50+290*index, y=80)
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*index,y=100)

                    for index, value in enumerate(dict1[key]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selected[value["text"]] = is_selected
        
        button3 = ttk.Button(self, text = "generate lists", command = generate)
        button3.place(x=50,y=50)

            

class PageThree(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Statistics and Graphs", font = LARGE_FONT)
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
        self.hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hscrollbar.pack(side='bottom', fill="x",  expand="false")

        self.canvas = tk.Canvas(self, bd=0,
                                height=220, width=200,
                                yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

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


    
#Basic app is set to the class NokiaSnakeclient
app = NokiaSnakeClient()
app.geometry("1280x720")
app.mainloop()