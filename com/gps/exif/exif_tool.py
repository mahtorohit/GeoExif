import time
import piexif
import json
from datetime  import datetime

from os import walk


from PIL import Image

fname = "/Users/rohit/Desktop/IMG_20171106_145221120.jpg"
img = Image.open(fname)

exif_dict = piexif.load(fname)
# print(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])


# for ifd in ("0th", "Exif", "GPS", "1st"):
#     for tag in exif_dict[ifd]:
#         print(" {} {} {} {}".format(ifd , tag, piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag]))

# exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = (140, 1)
# exif_bytes = piexif.dump(exif_dict)
# img.save(fname, exif=exif_bytes)
#
# exif_dict = piexif.load(fname)
#
# for ifd in ("0th", "Exif", "GPS", "1st"):
#     for tag in exif_dict[ifd]:
#         print(" {} {} {} {}".format(ifd , tag, piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag]))
#


def get_capture_date_milisec(imgae):
    exif_dict = piexif.load(fname)
    print(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
    date_string = (exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]).decode("utf-8")
    d = datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')
    return  time.mktime(d.timetuple()) * 1e3 + d.microsecond / 1e3


def get_capture_date(imgae):
    exif_dict = piexif.load(fname)
    print(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
    date_string = (exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]).decode("utf-8")
    return datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')


def get_gps_lat_lon(imgae):
    exif_dict = piexif.load(fname)
    lat = (exif_dict['GPS'][piexif.GPSIFD.GPSLongitude])
    print(lat)
    long = (exif_dict['GPS'][piexif.GPSIFD.GPSLongitude])
    print(long)
    return (lat,long)

print(get_gps_lat_lon(fname))