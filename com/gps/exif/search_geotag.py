import datetime
import pickle
import piexif
# from LatLon.lat_lon import LatLon
import com.gps.pasing.parser
from com.gps.pasing.parser import Location, DataModel


class GeoTag:
    location = None

    def __init__(self,location=None):
        if location is not None:
            self.location =location

    def find(self,time=None):
        if time is None and self.location is None:
            raise Exception("No Location data found to process")
        elif time is not None and self.location is not None:
            raise Exception("Two Location data has been passes")
        tag = None
        if time is None:
            tag = self.location
        else:
            tag = time
        data = DataModel().get_location_map()
        return self.search(tag,data)

    def search(self, location, data, tolerance=20, assign_priority=0):
        tolerance *= 60000
        key = location.date.strftime('%Y-%m-%d')
        if key in data:
            list_loc = data[key]
            time_diff_list = []
            tmp_obj = []
            for i in list_loc:
                diff = location.milisec - i.milisec
                if assign_priority == 0:
                    diff= abs(diff)
                    if 0 <= diff < tolerance:
                        time_diff_list.append(abs(location.milisec - i.milisec))
                        tmp_obj.append(i)
                        # print("Current Loc {} - diff : {}".format(i,diff))
                elif assign_priority > 0:
                    if 0 <= diff < tolerance:
                        time_diff_list.append(location.milisec - i.milisec)
                        tmp_obj.append(i)
                        # print("Current Loc {} - diff : {}".format(i, diff))
                elif assign_priority < 0:
                    if 0 >= diff > -tolerance:
                        time_diff_list.append(abs(location.milisec - i.milisec))
                        tmp_obj.append(i)
                        # print("Current Loc {} - diff : {}".format(i, diff))
            return tmp_obj[time_diff_list.index(min(time_diff_list))]
        else:
            return None

        # def search(self, location, data, tolerance=20, assign_priority=1):
        #     tolerance *= 60000
        #     key = location.date.strftime('%Y-%m-%d')
        #     if key in data:
        #         list_loc = data[key]
        #         time_diff_list = []
        #         for i in list_loc:
        #             diff = location.milisec - i.milisec
        #             if assign_priority == 0:
        #                 if 0 > diff > -tolerance:
        #                     time_diff_list.append(location.milisec - i.milisec)
        #                     print("Current Loc {} - diff : {}".format(i, diff))
        #                 elif 0 <= diff < tolerance:
        #                     time_diff_list.append(location.milisec - i.milisec)
        #                     print("Current Loc {} - diff : {}".format(i, diff))
        #             elif assign_priority > 0:
        #                 if 0 <= diff < tolerance:
        #                     time_diff_list.append(location.milisec - i.milisec)
        #                     print("Current Loc {} - diff : {}".format(i, diff))
        #             elif assign_priority < 0:
        #                 if 0 >= diff > -tolerance:
        #                     time_diff_list.append(location.milisec - i.milisec)
        #                     print("Current Loc {} - diff : {}".format(i, diff))
        #
        #         return list_loc[time_diff_list.index(min(time_diff_list))]
        #     else:
        #         return None

# g=GeoTag().find()

path= "/Users/rohit/Desktop/IMG_20171106_145221120.jpg"

# palmyra = LatLon(18.5304846944444, 73.9136041944444)
#
# print (palmyra.to_string('d% %m% %S% %H'))


def decdeg2dms(dd):
    negative = dd < 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return (degrees,minutes,seconds)

print(decdeg2dms(185636347/10000000))