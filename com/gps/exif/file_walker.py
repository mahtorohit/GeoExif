from os import walk

from com.gps.exif.exif_tool import get_capture_date

mypath = "/Users/rohit/Desktop/SAYALI3300/DCIM/100D3300/"


f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    print(filenames)
    for file in filenames:
        filepath = mypath+file
        date = get_capture_date(file)
        print("{} - {}".format(file,date))
    break




