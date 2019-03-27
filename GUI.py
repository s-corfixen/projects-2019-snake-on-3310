#import packages
from tkinter import *
from PIL import Image, ImageTk
#proof of concept
#starting the main window.
class Window(Frame):
    #Defining the window
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()
    
    
    #The window itself
    def init_window(self):
        self.master.title("GUI")

        self.pack(fill=BOTH, expand=1)

        #quitbutton = Button(self, text="Quit", command=self.client_exit)
        #quitbutton.place(x=0,y=0)
        
        #button
        button = Button(self, text="Button", command=self.showtxt)
        button.place(x=500,y=700)

        #simple check button
        Label(text="Din mening:").place(x=0,y=680)
        global var1
        var1 = IntVar()
        Checkbutton(text="sjovt", variable=var1).place(x=0, y=700)
        global var2
        var2 = IntVar()
        Checkbutton(text="ikke sjovt", variable=var2).place(x=0, y=720)
        
        #Resultbutton
        Button(self, text="Resultat", command=self.var_states).place(x=5,y=740)
        

        #Making the menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        #adding the file button under menu
        file = Menu(menu)
        #adding the options for file
        file.add_command(label="save")
        file.add_command(label="Exit", command=self.client_exit)
        #adding file to menu bar
        menu.add_cascade(label="File", menu=file)
        
        #adding the edit button under menu
        edit = Menu(menu)
        #addomg the options for edit
        edit.add_command(label="Show Image", command=self.showImg)
        edit.add_command(label="Show Text", command=self.showtxt)
        #adding edit to menu bar
        menu.add_cascade(label="Edit", menu=edit)
    
    #defing the function ShowImg used in editmenu
    def showImg(self):
        load = Image.open("PSG.png")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=50,y=0)

    #defining the function showtxt used in editmenu
    def showtxt(self):
        text = Label(self, text="AHAHAHAHAHAHAHAHAHA")
        text.pack()
        

    #defining the exit option in the file menu
    def client_exit(self):
        exit()
    #defining var_states used in checkbox
    def var_states(self):
        result = "Folk med god humor: %d, \nDer er så meget kvinder ikke forstår: %d" % (var1.get(),var2.get())
        text = Label(self, text=result)
        text.place(x=200, y=700)

#determine default size of window and running it
root=Tk()
root.geometry("600x800")
app = Window(root)
root.mainloop()
