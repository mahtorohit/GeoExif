from enum import Enum
from gps.pasing.google_parser import DataModel, Location


class LocationOverWrite(Enum):
    SKIP = 1
    OVERWRITE = 0


class OperationType(Enum):
    SEARCH = 1
    EXECUTE = 0


class LocationPriority(Enum):
    BEFORE = 1
    ANY = 0
    AFTER = -1


class AccuracyTolerance(Enum):
    MIN = 0
    MIN1 = 1
    MIN5 = 5
    MIN15 = 15
    MIN30 = 30
    HR1 = 60
    HR2 = 120


class GeoTag:

    location = None
    data = None

    def __init__(self,location=None):
        if location is not None:
            self.location =location
        self.data = DataModel(preloded=True).get_location_map()

    def find(self, time=None, tolerance=AccuracyTolerance.MIN15, assign_priority=LocationPriority.ANY):
        if time is None and self.location is None:
            raise Exception("No Location data found to process")
        elif time is not None and self.location is not None:
            raise Exception("Two Location data has been passes")
        if time is None:
            tag = self.location
        else:
            tag = time
        return self.__search(tag,self.data,tolerance=tolerance.value, assign_priority=assign_priority)

    def __search(self, location, data, tolerance, assign_priority):
        tolerance *= 60000
        key = location.date.strftime('%Y-%m-%d')
        if key in data:
            list_loc = data[key]
            time_diff_list = []
            tmp_obj = []
            for i in list_loc:
                diff = location.milisec - i.milisec
                if assign_priority == LocationPriority.ANY:
                    diff= abs(diff)
                    if 0 <= diff < tolerance or tolerance == 0:
                        time_diff_list.append(abs(location.milisec - i.milisec))
                        tmp_obj.append(i)
                elif assign_priority ==  LocationPriority.BEFORE:
                    if 0 <= diff < tolerance or tolerance == 0:
                        time_diff_list.append(location.milisec - i.milisec)
                        tmp_obj.append(i)
                        # print("Current Loc {} - diff : {}".format(i, diff))
                elif assign_priority == LocationPriority.AFTER:
                    if 0 >= diff > -tolerance or tolerance == 0:
                        time_diff_list.append(abs(location.milisec - i.milisec))
                        tmp_obj.append(i)
                        # print("Current Loc {} - diff : {}".format(i, diff))
            if len(time_diff_list) is not 0:
                return tmp_obj[time_diff_list.index(min(time_diff_list))], min(time_diff_list)
            else:
                return None, 0
        else:
            return None , 0

