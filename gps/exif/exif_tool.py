import time
from datetime import datetime
import piexif
from gps.exif.search_geotag import GeoTag, AccuracyTolerance, LocationPriority, LocationOverWrite, OperationType
from gps.pasing.google_parser import Location


class ExifOps:

    @staticmethod
    def get_capture_date_milisec(image):
        exif_dict = piexif.load(image)
        date_string = (exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]).decode("utf-8")
        d = datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')
        return time.mktime(d.timetuple()) * 1e3 + d.microsecond / 1e3

    @staticmethod
    def get_capture_date(image):
        exif_dict = piexif.load(image)
        date_string = (exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]).decode("utf-8")
        return datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')

    @staticmethod
    def get_gps_lat_lon(image):
        exif_dict = piexif.load(image)
        lat = (exif_dict['GPS'][piexif.GPSIFD.GPSLatitude])
        long = (exif_dict['GPS'][piexif.GPSIFD.GPSLongitude])
        return lat, long

    @staticmethod
    def is_gps_available(image):
        exif_dict = piexif.load(image)
        lat = None
        long = None
        if piexif.GPSIFD.GPSLongitude in exif_dict['GPS']:
            lat = (exif_dict['GPS'][piexif.GPSIFD.GPSLatitude])
        if piexif.GPSIFD.GPSLongitude in exif_dict['GPS']:
            long = (exif_dict['GPS'][piexif.GPSIFD.GPSLongitude])
        if lat is None or long is None:
            return False
        else:
            return True

    @staticmethod
    def add_gps_available(image,gps):
        exif_dict = piexif.load(image)
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = ExifOps.decdeg2dms(gps[0]/10000000)
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = ExifOps.decdeg2dms(gps[1]/10000000)
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image)

    @staticmethod
    def decdeg2dms(dd):
        negative = dd < 0
        dd = abs(dd)
        minutes, seconds = divmod(dd * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        if negative:
            if degrees > 0:
                degrees = -degrees
            elif minutes > 0:
                minutes = -minutes
            else:
                seconds = -seconds
        return (int(degrees), 1), (int(minutes), 1), ((int(seconds * 10000)), 10000)

    @staticmethod
    def batch_job(path,time_accuracy,time_priority,overwrite,op):
        from gps.exif.file_walker import FileManager
        files = FileManager().get_all_files(path)
        g = GeoTag()
        count = 0
        for file in files:
            if file.endswith('.JPG') or file.endswith('.JPEG'):
                if ExifOps.is_gps_available(file) is False:
                    time = ExifOps.get_capture_date(file)
                    loc = Location(date=time)
                    loc, diff = g.find(loc,time_accuracy,time_priority)
                    if loc is not None:
                       count+=1
                    print("********* Found : {0} - {1} - time diff - {2:.2f} min".format(file, loc, diff/60000))
                    if op == OperationType.EXECUTE:
                        if loc is not None:
                            ExifOps.add_gps_available(str(file),(loc.lat,loc.long))
                            print("********* File : {} - location : {} updated".format(str(file), loc))

        print("Total : {} - location : {}".format(len(files),count))
        return len(files), count

    @staticmethod
    def add_gps_available_test(image,gps):
        exif_dict = exif_dict = piexif.load(image)
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = ExifOps.decdeg2dms(gps[0] / 10000000)
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = ExifOps.decdeg2dms(gps[1] / 10000000)
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image)

