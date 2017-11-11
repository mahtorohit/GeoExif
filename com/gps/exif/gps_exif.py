from tkinter import Tk, Label, Button, Entry

import datetime

from com.gps.exif.search_geotag import GeoTag
from com.gps.pasing.parser import Location
class MyFirstGUI:
    entry_location = None
    lable_location = None

    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")
        master.minsize(width=666, height=666)

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()
        self.entry_location =  Entry(root, width=20)
        self.entry_location.pack()

        self.lable_location = Label(master, text="Result : ")
        self.lable_location.pack()

        self.load_location = Button(master, text="Load Json", command=self.greet)
        self.load_location.pack()

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def greet(self):
        if len(self.entry_location.get()) == 0:
            print("failed 1")
            return
        if self.is_number(self.entry_location.get()) is False:
            print("failed 2")
            return

        loc = {}
        loc['latitudeE7'] = '185750561'
        loc['longitudeE7'] = '737377022'
        loc['accuracy'] = '200'
        loc["timestampMs"] = self.entry_location.get()


        l = Location(loc)
        data = GeoTag().find(l)
        print(data)
        self.lable_location['text'] = str(data)

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
