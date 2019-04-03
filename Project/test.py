import pydst
import tkinter as tk
import pandas as pd

Dst = pydst.Dst(lang='en')

master = tk.Tk()

e1 = tk.Entry(master)
e1.pack()

dict1 = {}
def ok():
    tableid = e1.get()
    data = Dst.get_variables(table_id=tableid)
    text = list(data["text"])
    print(type(tableid))
    for i in text:
        dataframe = data.loc[data["text"] == i,"values"]
        data_list = list(dataframe)
        i_list = []
        for sublist in data_list:
            for item in sublist:
                del item["id"]
                i_list.append(item)
        dict1.update({i: i_list})

button = tk.Button(master, text="Load", command = ok)
button.pack()

    #print(dict1)
    #data = Dst.get_data(table_id=id)
    #headers = (list(data))
    #del headers[-1]
    #dict1 = dict.fromkeys(headers, ["*"])
    #savepath = "C:/Users/Corfixen/projects-2019-snake-on-3310/"+str(id)+".csv"
    #Dst.get_csv(path=savepath, table_id=id, variables = dict1)
    #dataset = Dst.get_data(table_id=id, variables = dict1)
    #headers2 = headers[:]
    #del headers2["tid"]
    #del headers2["indhold"]
    #dataset2 = dataset.pivot(index="headers2",columns="tid",values="indhold")
    #data.to_excel('C:/Users/Corfixen/projects-2019-snake-on-3310/data.xlsx',  sheet_name='Sheet1')

  
        

master.mainloop()