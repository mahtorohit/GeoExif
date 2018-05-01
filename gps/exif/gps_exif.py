import os
import threading
from tkinter import Tk, Label, Button, IntVar, Radiobutton
from tkinter import messagebox as tkMessageBox
from tkinter.filedialog import askopenfile, askdirectory

from gps.exif.exif_tool import ExifOps
from gps.exif.search_geotag import GeoTag, AccuracyTolerance, LocationPriority, LocationOverWrite, OperationType
from gps.pasing.google_parser import Location, DataModel


class MyFirstGUI():
    working = False
    time_accuracy = None
    time_priority = None
    overwrite_policy = None
    op_path = None
    operation = None

    def __init__(self, master):
        self.master = master
        master.title("Welcome to Exif Tool")
        master.minsize(width=600, height=600)

        #  Step 1
        # Load the google json file
        self.load_location_file = Button(master, text="Load Json", command=self.load_json_file)
        self.load_location_file.grid(row=1, columnspan=7, ipady=10)
        # #########################

        #  Step 2
        # Load the images folder for exif manipulations
        self.load_location_file = Button(master, text="Load Image Folder", command=self.load_image_folder)
        self.load_location_file.grid(row=2, columnspan=7, ipady=10)
        # #########################

        self.remove_geo_tags = Button(master, text="Remove Geo Tags", command=self.load_json_file)
        self.remove_geo_tags.grid(row=3, columnspan=3.5, ipady=10)

        self.remove_all_tags = Button(master, text="Remove All Exif Tags", command=self.load_json_file)
        self.remove_all_tags.grid(row=3, columnspan=3.5, ipady=10)

        #  Step 3
        # Select Location assign parameter : Accuracy
        self.time_accuracy = IntVar()
        Label(master, text="Select location time accuracy ").grid(row=3, columnspan=7, ipady=10)

        Radiobutton(master, text="01 Min", variable=self.time_accuracy, value=1).grid(row=4, column=0, ipady=10)
        Radiobutton(master, text="05 Min", variable=self.time_accuracy, value=5).grid(row=4,column=1,ipady=10)
        Radiobutton(master, text="15 Min", variable=self.time_accuracy, value=15).grid(row=4,column=2,ipady=10)
        Radiobutton(master, text="30 Min", variable=self.time_accuracy, value=30).grid(row=4, column=3, ipady=10)
        Radiobutton(master, text="01 hr", variable=self.time_accuracy, value=60).grid(row=4, column=4, ipady=10)
        Radiobutton(master, text="02 hr", variable=self.time_accuracy, value=120).grid(row=4, column=5, ipady=10)
        Radiobutton(master, text="Day", variable=self.time_accuracy, value=0).grid(row=4, column=6, ipady=10)
        self.time_accuracy.set(15)
        # #########################


        #  Step 4
        # Select Location arsing parameter : Priority
        self.time_priority = IntVar()
        Label(master, text="Select location time priority ").grid(row=5, columnspan=7, ipady=10)
        Radiobutton(master, text="PAST", variable=self.time_priority, value=1).grid(row=6, column=0, ipady=10)
        Radiobutton(master, text="FUTURE", variable=self.time_priority, value=-1).grid(row=6, column=1, ipady=10)
        Radiobutton(master, text="ANY", variable=self.time_priority, value=0).grid(row=6, column=2, ipady=10)
        self.time_priority.set(0)
        # #########################

        #  Step 5
        # Select Overwrite policy
        self.overwrite_policy = IntVar()
        Label(master, text="Select Location Overwrite policy ").grid(row=7, columnspan=7, ipady=10)
        Radiobutton(master, text="Skip", variable=self.overwrite_policy, value=1).grid(row=8, column=0, ipady=10)
        Radiobutton(master, text="OverWrite", variable=self.overwrite_policy, value=0).grid(row=8, column=1, ipady=10)
        self.overwrite_policy.set(1)
        # #########################

        #  Step 6
        # Select Opration
        self.operation = IntVar()
        Label(master, text="Operation Type ").grid(row=9, columnspan=7, ipady=10)
        Radiobutton(master, text="Search", variable=self.operation, value=1).grid(row=10, column=0, ipady=10)
        Radiobutton(master, text="Execute", variable=self.operation, value=0).grid(row=10, column=1, ipady=10)
        self.operation.set(0)
        # #########################


        #  Step 7
        # Start with Processing
        self.process = Button(master, text="Start Processing", command=self.process_imges).grid(row=11, columnspan=7, ipady=10)
        # #########################

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

    def load_image_folder(self):
        if self.working:
            tkMessageBox.showinfo("Exif Tool", "Wait till current tasks get's finished !")
            return
        dirname = askdirectory()
        self.op_path = dirname

    def load_json_file(self):
        if self.working:
            tkMessageBox.showinfo("Exif Tool", "Wait till current tasks get's finished !")
            return
        filename = askopenfile()
        filename = filename.name

        def load_data(self,filename):
            self.working = True
            DataModel(filename).load_data_map()
            self.working = False
            tkMessageBox.showinfo("Exif Tool", "Data successfully Loaded from {}".format(filename))

        threading._start_new_thread(load_data, (self,filename))

    def remove_geo_tag(self):
        self.check_files()

        def remove(self,filename):
            self.working = True


        threading._start_new_thread(remove, (self,filename))

    def process_imges(self):
        self.check_files()

        def execute(self):
            self.working = True
            data = ExifOps.batch_job(self.op_path, AccuracyTolerance(self.time_accuracy.get()),
                                     LocationPriority(self.time_priority.get()),
                                     LocationOverWrite(self.overwrite_policy.get()),
                                     OperationType(self.operation.get()))
            tkMessageBox.showinfo("Exif Tool", "Total images : {}, found Location for : {}".format(data[0],data[1]))
            self.working = False


        threading._start_new_thread(execute, (self,))


    def do(self,loc):
        self.working = True
        l = Location(loc)
        data = GeoTag().find(l)
        print(data)
        self.lable_location['text'] = str(data)
        diff = int(loc["timestampMs"]) - data.milisec
        diff /= 60000
        tkMessageBox.showinfo("Say Hello", "{} - \n diff is {} min".format(str(data),diff))
        self.working = False

    def check_files(self):
        if self.working:
            tkMessageBox.showinfo("Exif Tool", "Wait till current tasks get's finished !")
            return
        if self.op_path is None:
            tkMessageBox.showinfo("Exif Tool", "Please select Images to process!")
            return

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
