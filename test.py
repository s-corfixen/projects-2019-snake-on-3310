import pydst
import tkinter as tk
import pandas as pd

Dst = pydst.Dst(lang='da')

master = tk.Tk()

e1 = tk.Entry(master)
e1.pack()


def ok():
    id = e1.get()
    data = Dst.get_data(table_id=id)
    headers = (list(data))
    del headers[-1]
    dict1 = dict.fromkeys(headers, ["*"])
    dataset = Dst.get_data(table_id=id, variables = dict1)
    dataset.to_excel('c:/Users/Corfixen/Documents/projects-2019-snake-on-3310/data.xlsx',  sheet_name='Sheet1')
    
button = tk.Button(master, text="Load", command = ok)
button.pack()
        

master.mainloop()