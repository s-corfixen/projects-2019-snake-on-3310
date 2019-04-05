#import several libraries need for the program to function. 
import tkinter as tk
from tkinter import ttk
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pydst

#set the default language for the DST API
Dst = pydst.Dst(lang='en')

#Text fonts later referenced in the code
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana",9)
SMALL_FONT = ("Verdana",8)

#We create several global variables which will be referenced and changed.
metadatadictionary = {}
apidictionary = {}
tableid = "empty"
dataset = pd.DataFrame
datasetpivot = pd.DataFrame

#We create the main class, which defines the container in which all frames are defined. Think of it as the app itself.
class NokiaSnakeClient(tk.Tk):

    #defining the initialization method with room for the inherited args and kwargs from tk.Tk
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #We set the icon and title for the app frame
        tk.Tk.iconbitmap(self, "./Project/snakeicon.ico")
        tk.Tk.wm_title(self, "NokiaSnake client")

        #defining the container later used to create the frames in the app
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #We define the dictionary, which will be updated to contain our frames.
        self.frames = {}

        #Using a for loop, we create all the frames with the container previously defined
        for F in (PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        #We set the default frame to be PageOne
        self.show_frame(PageOne)
    #We create a function which shows the frame called in the "cont" argument
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    #The clearall function resets all global variables to their default value and shows the frame defined in the "cont" argument
    def clearall(self, cont):
        global metadatadictionary
        metadatadictionary = {} 
        global apidictionary
        apidictionary = {}
        global tableid
        tableid = "empty"
        global dataset
        dataset = pd.DataFrame
        global datasetpivot
        datasetpivot = pd.DataFrame

        frame = self.frames[cont]
        frame.tkraise()

#Creating the PageOne class, which is our startpage.
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Creating the pagetitle
        pagetitle = tk.Label(self, text = "Choosing Dataset", font = LARGE_FONT)
        pagetitle.pack(pady=10,padx=10)

        #We define a function next page, which raises different pages depending on the value of the menuvariable
        def nextpage():
            if menuvariable.get()==0:
                controller.show_frame(PageThree)
            else:
                controller.show_frame(PageTwo)

        #We create two buttons on pageone. The first runs the function nextpage.
        nextbutton = ttk.Button(self, text = "Next Page", command = nextpage)
        nextbutton.place(x=1180,y=680)
        #The second runs the function clearall defined in the class NokiaSnake_client
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)
        
        
        #Menuvariable is created as an integer variables.
        menuvariable = tk.IntVar()
        menubuttonlabels = ["NAN1", "Custom data"]
        tk.Label(self, text="Choose Dataset to be used", justify = tk.LEFT, padx = 20).place(x=550, y=180)

        def LoadDataset():
            if menuvariable.get()==0:
                global dataset
                dataset = Dst.get_data(table_id = "NAN1", variables={'TRANSAKT': ["*"], 'PRISENHED': ["*"], 'Tid': ["*"]}, lang="en")

            else:
                popupmsg()

        for val, dataset in enumerate(menubuttonlabels):
            ttk.Radiobutton(self, 
                text=dataset,
                variable=menuvariable, 
                command = LoadDataset,
                value=val).place(x=600, y=200+val*20)
        
        
                
        def popupmsg():
            popup = tk.Tk()

            popup.wm_title("Load dataset")
            label = ttk.Label(popup, text="Warning: Experimental Feature", font=NORM_FONT)
            label.place(x=0,y=0)      

            entry1 = tk.Entry(popup)
            entry1.place(x=38,y=50)

            
            def ok():               
                global tableid
                tableid = entry1.get()
                try:
                    data = Dst.get_variables(table_id=tableid)
                    text = list(data["text"])
                    
                    for i in text:
                        dataframe = data.loc[data["text"] == i,"values"]
                        data_list = list(dataframe)
                        i_list = []
                        for sublist in data_list:
                            for item in sublist:
                                i_list.append(item)
                        metadatadictionary.update({i: i_list})
                    for i in text:
                        idapi = data.loc[data["text"]== i, "id"].item()
                        apidictionary.update({i: idapi})
                    popup.destroy()
                
                except:
                    errormessage = ttk.Label(popup, foreground = "red", text="Table not found", font=NORM_FONT)
                    errormessage.place(x=42,y=70)

            button = tk.Button(popup, text="Load", command = ok)
            button.place(x=80,y=120)

            popup.geometry("200x150")
            popup.mainloop()        



class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Customize Dataset", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)
        

        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)

        def getdataset():
            selectedvariables = {}
            
            for header, elist in metadatadictionary.items():
                
                list1 = []
                for key in selected:
                    if selected[key].get():
                        list1.append(key)
                list2 = []
                for dic in elist:
                    if dic["text"] in list1:
                        list2.append(dic["id"])
                if list2 != []:
                    selectedvariables.update({str(apidictionary[header]): list2})    
            global dataset
            dataset = Dst.get_data(table_id=tableid, variables = selectedvariables)
            
        getdatabutton = ttk.Button(self, text = "Get Data", command = getdataset)
        getdatabutton.place(x=600,y=650)
        
        def savedataset():
            savepath = "./"+str(tableid)+".xlsx"
            dataset.to_excel(savepath, sheet_name="Sheet1")

        savedatabutton = ttk.Button(self, text = "Save Data", command = savedataset)
        savedatabutton.place(x=600,y=680)

        selected = {}
        #scrollable list
        def generate():
            for index, key in enumerate(metadatadictionary):
                if index > 3:
                    label = tk.Label(self, text = key, font = SMALL_FONT)
                    label.place(x=50+290*(index-4), y=360)
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*(index-4), y=380)

                    for index, value in enumerate(metadatadictionary[key]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selected[value["text"]] = is_selected

                else:
                    label = tk.Label(self, text = key, font = SMALL_FONT)
                    label.place(x=50+290*index, y=80)
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*index,y=100)

                    for index, value in enumerate(metadatadictionary[key]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selected[value["text"]] = is_selected
        
        button3 = ttk.Button(self, text = "generate lists", command = generate)
        button3.place(x=50,y=50)



class PageThree(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Pagetitle = tk.Label(self, text = "NAN1 Table from DST", font = LARGE_FONT)
        Pagetitle.pack(pady=10,padx=10)
        graphlabel = tk.Label(self, text = "Create Graph", font = NORM_FONT)
        graphlabel.place(x=825,y=70)
        

        button1 = ttk.Button(self, text = "Back", 
                             command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)
        
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)

        var1 = tk.StringVar()
        selected = {}

        def generate():
            label = tk.Label(self, text="Price Unit", font = SMALL_FONT)
            label.place(x=50, y=50)
            prislist_index = ScrollableFrame(self)
            prislist_index.place(x=50, y=70)
            for index, titel in enumerate(dataset["PRISENHED"].unique()):
                ttk.Radiobutton(prislist_index.interior, text=titel, variable=var1, value=titel).grid(row=index, column=0, sticky="w")

            label = tk.Label(self, text="Transaction", font = SMALL_FONT)
            label.place(x=300, y=50)
            translist_index = ScrollableFrame(self)
            translist_index.place(x=300,y=70)
            for index, titel in enumerate(dataset["TRANSAKT"].unique()):
                is_selected = tk.BooleanVar()
                tk.Checkbutton(translist_index.interior, text=titel, variable=is_selected).grid(row=index,column=0,sticky="W")
                selected.update({titel: is_selected})

        generatebutton = ttk.Button(self, text = "generate lists", command = generate)
        generatebutton.place(x=50,y=20)
        
        textwindow = ScrollableFrame(self)
        textwindow.place(x=550,y=360)
        text = tk.Text(textwindow.interior, wrap="none", borderwidth=0)
        text.pack(expand=True, fill="both")

        def slicedata():
            
            global datasetpivot
            datasetpivot = pd.DataFrame
            rows = []
            for key in selected:
                if selected[key].get()==True:
                    rows.append(key)

            datasetsort = dataset.loc[dataset["TRANSAKT"].isin(rows)]
            datasetsort1 = datasetsort[datasetsort["PRISENHED"]==var1.get()] 
            datasetsort1["INDHOLD"]=pd.to_numeric(datasetsort1["INDHOLD"], errors="coerce")
            datasetsort1.dropna(inplace=True)
            
            datasetpivot = datasetsort1.pivot(index="TID", columns="TRANSAKT", values = "INDHOLD")
            
            text.delete('1.0', tk.END)
            text.insert(tk.END, datasetpivot.describe())
            print(datasetpivot.describe())
            
        slicebutton = ttk.Button(self, text = "slice dataset", command = slicedata)
        slicebutton.place(x=400, y=320)
        
        graphtypes = ["line", "stacked area", "pct. stacked area"]

        graphmenuvariable = tk.StringVar()
        graphmenuvariable.set(graphtypes[0])

        graphmenu = tk.OptionMenu(self, graphmenuvariable, *graphtypes)
        graphmenu.place(x=900,y=100)

        def makegraph():
            
            if graphmenuvariable.get()=="line":
                datasetpivot.plot(kind="line")
                plt.ylabel(var1.get())
                plt.xlabel("Time")
                plt.show()
            elif graphmenuvariable.get()=="stacked area":
                datasetpivot.plot.area()
                plt.ylabel(var1.get())
                plt.xlabel("Time")
                plt.show()
            elif graphmenuvariable.get()=="pct. stacked area":
                datasetpivot_pct = datasetpivot.divide(datasetpivot.sum(axis=1), axis=0)
                datasetpivot_pct.plot.area()
                plt.ylabel("percent")
                plt.xlabel("Time")
                plt.show()            
        

        button = ttk.Button(self, text="Make Graph", command=makegraph)
        button.place(x=810,y=105)     

        

        



class ScrollableFrame(tk.Frame):
    def __init__(self, master,**kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y",  expand="false")
        self.hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hscrollbar.pack(side='bottom', fill="x",  expand="false")
        self.canvas = tk.Canvas(self, width=200, height=220,
                                yscrollcommand=self.vscrollbar.set,
                                xscrollcommand=self.hscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

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