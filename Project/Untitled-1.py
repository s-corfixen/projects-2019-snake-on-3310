import tkinter as tk
from tkinter import *

root = tk.Tk()

dict = {"header1": [{"id":1, "text":"df"}], "header2": [{"id":2, "text":"fd"}], "header3": [{"id":3, "text":"gf"}]}
lb1 = tk.Listbox(root,selectmode="extended")

index = 0
for i, key in enumerate(dict):
    for j, value in enumerate(dict[key]):
        lb1.insert(index, value["text"])
        index+=1

lb1.pack()
selectedvariables = {}

def Get():  # Read back the listbox
    for header, elist in dict.items():
        selecteddata = [lb1.get(index) for index in lb1.curselection()]
        list2 = []
        for dic in elist:
            if dic["text"] in selecteddata:
                list2.append(dic["id"])
        if list2 != []:
            selectedvariables.update({str(header): list2})


readbutton = tk.Button(root, text = "Get List", command = Get)
readbutton.pack()

root.mainloop()