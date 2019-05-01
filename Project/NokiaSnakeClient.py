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



Dst = pydst.Dst(lang='en')

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana",9)
SMALL_FONT = ("Verdana",8)


metadatadictionary = {}
apidictionary = {}
tableid = "empty"
dataset = pd.DataFrame
datasetpivot = pd.DataFrame


class NokiaSnakeClient(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "NokiaSnake client")

       
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


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        pagetitle = tk.Label(self, text = "Choosing Dataset", font = LARGE_FONT)
        pagetitle.pack(pady=10,padx=10)

        
        def nextpage():
            if menuvariable.get()==0:
                controller.show_frame(PageThree)
            else:
                controller.show_frame(PageTwo)

        
        nextbutton = ttk.Button(self, text = "Next Page", command = nextpage)
        nextbutton.place(x=1180,y=680)
        
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)
        
        
       
        menuvariable = tk.IntVar()
        menuvariable.set(1)
        
        menubuttonlabels = ["NAN1", "Custom data"]
        tk.Label(self, text="Choose Dataset to be used", justify = tk.LEFT, padx = 20).place(x=550, y=180)

        def LoadDataset():
            if menuvariable.get()==0:
                global dataset
                dataset = Dst.get_data(table_id = "NAN1", variables={'TRANSAKT': ["*"], 'PRISENHED': ["*"], 'Tid': ["*"]}, lang="en")

            else:
                popupmsg()

       
        for index, label in enumerate(menubuttonlabels):
            ttk.Radiobutton(self, text=label, variable=menuvariable, command = LoadDataset,
                value=index).place(x=600, y=200+index*20)
        
        
         
        def popupmsg():
            popup = tk.Tk()
            popup.wm_title("Load dataset")
            label = ttk.Label(popup, text="Warning: Experimental Feature", font=NORM_FONT)
            label.place(x=0,y=0)      

            entry1 = tk.Entry(popup)
            entry1.place(x=38,y=50)

            
            def loadcustomdata():           
                global tableid
                tableid = entry1.get()
                try:
                    data = Dst.get_variables(table_id=tableid)
                    categories = list(data["text"])
                    
                    for title in categories:
                        dataframe = data.loc[data["text"] == title,"values"]
                        data_list = list(dataframe)
                        dict_list = []
                        for sublist in data_list:
                            for dic in sublist:
                                dict_list.append(dic)
                        metadatadictionary.update({title: dict_list})
                    for title in categories:
                        api_id = data.loc[data["text"]== title, "id"].item()
                        apidictionary.update({title: api_id})
                    popup.destroy()
                except:
                    errormessage = ttk.Label(popup, foreground = "red", text="Table not found", font=NORM_FONT)
                    errormessage.place(x=42,y=70)

            button = tk.Button(popup, text="Load", command = loadcustomdata)
            button.place(x=80,y=120)
            popup.geometry("200x150")
            popup.mainloop()        


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titlelabel = tk.Label(self, text = "Customize Dataset", font=LARGE_FONT)
        titlelabel.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)
        
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)

        def getdataset():
            selectedvariables = {}
            for header, elist in metadatadictionary.items():
                list1 = []
                for key in selectedbutton:
                    if selectedbutton[key].get():
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
        
        selectedbutton = {}
        
        def generate():
            for index, header in enumerate(metadatadictionary):
                if index > 3:
                    label = tk.Label(self, text = header, font = SMALL_FONT)
                    label.place(x=50+290*(index-4), y=360)
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*(index-4), y=380)

                    for index, value in enumerate(metadatadictionary[header]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selectedbutton[value["text"]] = is_selected

                else:
                    label = tk.Label(self, text = header, font = SMALL_FONT)
                    label.place(x=50+290*index, y=80)
                    checkboxlist_index = ScrollableFrame(self)
                    checkboxlist_index.place(x=50+290*index,y=100)

                    for index, value in enumerate(metadatadictionary[header]):
                        is_selected = tk.BooleanVar()
                        ttk.Checkbutton(checkboxlist_index.interior, text=value["text"], variable=is_selected).grid(row=index,column=0,sticky="W")
                        selectedbutton[value["text"]] = is_selected

        button3 = ttk.Button(self, text = "generate lists", command = generate)
        button3.place(x=50,y=50)


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Pagetitle = tk.Label(self, text = "NAN1 Table from DST", font = LARGE_FONT)
        Pagetitle.pack(pady=10,padx=10)
        graphlabel = tk.Label(self, text = "Create Graph", font = NORM_FONT)
        graphlabel.place(x=825,y=70)
        
        button1 = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(PageOne))
        button1.place(x=20, y=680)
        
        clearallbutton = ttk.Button(self, text = "Clear All", command = lambda: controller.clearall(PageOne))
        clearallbutton.place(x=20, y=650)

        buttonvariable = tk.StringVar()
        selected = {}
        
        def generate2():
            pricelabel = tk.Label(self, text="Price Unit", font = SMALL_FONT)
            pricelabel.place(x=50, y=50)

            prislist_index = ScrollableFrame(self)
            prislist_index.place(x=50, y=70)

            for index, titel in enumerate(dataset["PRISENHED"].unique()):
                ttk.Radiobutton(prislist_index.interior, text=titel, variable=buttonvariable, value=titel).grid(row=index, column=0, sticky="w")
            
            translabel = tk.Label(self, text="Transaction", font = SMALL_FONT)
            translabel.place(x=300, y=50)

            translist_index = ScrollableFrame(self)
            translist_index.place(x=300,y=70)

            for index, titel in enumerate(dataset["TRANSAKT"].unique()):
                is_selected = tk.BooleanVar()
                tk.Checkbutton(translist_index.interior, text=titel, variable=is_selected).grid(row=index,column=0,sticky="W")
                selected.update({titel: is_selected})

        generatebutton = ttk.Button(self, text = "generate lists", command = generate2)
        generatebutton.place(x=50,y=20)
        
        textwindow = ScrollableFrame(self, canvasheight=300, canvaswidth=600)
        textwindow.place(x=550,y=360)
        text = tk.Text(textwindow.interior)
        text.pack()
        
        def slicedata():
            global datasetpivot
            datasetpivot = pd.DataFrame
            
            rows = []
            for key in selected:
                if selected[key].get()==True:
                    rows.append(key)

            datasetsort = dataset.loc[dataset["TRANSAKT"].isin(rows)]
            datasetsort1 = datasetsort[datasetsort["PRISENHED"]==buttonvariable.get()]
            datasetsort1["INDHOLD"]=pd.to_numeric(datasetsort1["INDHOLD"], errors="coerce")
            datasetsort1.dropna(inplace=True)

            datasetpivot = datasetsort1.pivot(index="TID", columns="TRANSAKT", values = "INDHOLD")
            text.delete('1.0', tk.END)
            for column in datasetpivot:
                text.insert(tk.END, datasetpivot[column].describe())
            textwindow.set_scrollregion()

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
                plt.ylabel(buttonvariable.get())
                plt.xlabel("Time")
                plt.show()
            elif graphmenuvariable.get()=="stacked area":
                datasetpivot.plot.area()
                plt.ylabel(buttonvariable.get())
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
    def __init__(self, master, canvasheight=220, canvaswidth=200, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y",  expand="false")

        self.hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hscrollbar.pack(side='bottom', fill="x",  expand="false")

        self.canvas = tk.Canvas(self, width=canvaswidth, height=canvasheight, yscrollcommand=self.vscrollbar.set,
                                xscrollcommand=self.hscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")

        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

        self.interior = tk.Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")
        self.bind("<Configure>", self.set_scrollregion)

    def set_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class graphwindow(tk.Tk):
    def __init__(self, data, x, y, y2, graphnames, **kwargs):
        tk.Tk.__init__(self, **kwargs)
        
        fig = Figure()
        addsubplot = fig.add_subplot(1,1,1)
        addsubplot2 = addsubplot.twinx()
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH, expand = True)
            
        graphs = sorted(data[graphnames].unique())
        graphmenuvariable = tk.StringVar()
        graphmenuvariable.set(graphs[0])
        graphmenu = tk.OptionMenu(self, graphmenuvariable, *graphs)
        graphmenu.pack()
        
        def creategraph(data, x, y, y2):
            addsubplot.clear()
            addsubplot2.clear()
            
            E = data[graphnames] == graphmenuvariable.get()
            px = data.loc[E,:]
            
            positive = px[y].copy()
            negative = px[y].copy()
            
            positive[positive<=0] = np.nan
            negative[negative> 0] = np.nan
            
            addsubplot.bar(px[x], positive, color="g", width=0.5, alpha=0.5)
            addsubplot.bar(px[x], negative, color="r", width=0.5, alpha=0.5)
            addsubplot.set_xlabel(px[x].name)
            addsubplot.set_ylabel(px[y].name)
            
            addsubplot2.plot(px[x], px[y2], color="b", linewidth=3)
            addsubplot2.set_ylabel(px[y2].name)
            addsubplot2.legend()
            
            addsubplot.set_title(graphmenuvariable.get())
            canvas.draw()

        
        button = tk.Button(self, text="update", command= lambda: creategraph(data=data,x=x,y=y,y2=y2))
        button.pack()
        
        

if __name__ == "__main__":
    app = NokiaSnakeClient()
    app.geometry("1280x720")
    app.mainloop()