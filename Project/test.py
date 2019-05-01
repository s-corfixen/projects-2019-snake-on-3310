from tkinter import *

def func(value):
    print(value)

root = Tk()
options = ["1", "2", "3"]
var = StringVar()
drop = OptionMenu(root, var, *options, command=func)
drop.place(x=10, y=10)


root.mainloop()