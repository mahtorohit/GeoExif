from tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")
        master.minsize(width=666, height=666)

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.load_location = Button(master, text="Load Json", command=self.greet)
        self.load_location.pack()

         

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
