import datetime
import json
import pickle
import time as t
from pathlib import Path

url = "/Users/rohit/Downloads/Takeout/Location_History/Location_History.json"


class Location:
    latitude = None
    longitude = None
    date = None
    milisec = None
    accuracy = None

    def __init__(self, loc=None,date=None):
        if loc is not None:
            self.lat = loc['latitudeE7']
            self.long = loc['longitudeE7']
            self.accuracy = loc['accuracy']
            self.milisec = int(loc["timestampMs"])

            time = int(loc["timestampMs"]) / 1000
            date = datetime.datetime.fromtimestamp(
                int(time)
            )

            if self.lat is not None and self.long is not None and date is not None:
                self.longitude = self.long
                self.latitude = self.lat
                self.date = date
            else:
                raise Exception("Invalid Data for creating Location object {} - {} - {}".format(self.lat, self.long, self.date))
            return
        elif date is not None:
            self.lat= 0
            self.long = 0
            self.accuracy = 0
            self.milisec = int(t.mktime(date.timetuple()) * 1e3 + date.microsecond / 1e3)
            self.date = date
        else:
            raise Exception("Invalid Data for creating Location object")

    def __str__(self):
        return str("Time : {} - Latitude : {} - Longitude : {}".format(self.milisec,self.latitude,self.longitude))

    def __repr__(self):
        return str("Time : {} - Latitude : {} - Longitude : {}".format(self.milisec, self.latitude, self.longitude))


class DataModel:
    path = None

    def __init__(self, path=url,preloded=False):
        if preloded is True:
            return
        if path is None or len(path) == 0:
            raise Exception("Invalid File path, ensure the corrected path")
        my_file = Path(path)
        if my_file.exists() is False:
            raise Exception("Invalid File path, {} check if it exist".format(path))
        else:
            self.path = path

    def load_data_array(self):
        with open(self.path) as data_file:
            json_data = json.load(data_file)
            data = []
            json_data = json_data["locations"]
            print(len(json_data))
            for i in range(len(json_data)):
                data.append(Location(json_data[i]))
                print("Loading {}".format(i))
            pickle.dump(data, open("locations.p", "wb"))

    def load_data_map(self):
        with open(self.path) as data_file:
            json_data = json.load(data_file)
            loc_map = {}
            json_data = json_data["locations"]
            print(len(json_data))
            for i in range(len(json_data)):
                loc = Location(json_data[i])
                key = loc.date.strftime('%Y-%m-%d')
                if key in loc_map:
                    loc_map[key].append(loc)
                else:
                    loc_map[key] = [loc]

                print("Found {} - {}".format(i, loc))

            pickle.dump(loc_map, open("data/locations_map.p", "wb"))

    def get_location_map(self):
        with open("data/locations_map.p", "rb") as input_file:
            return pickle.load(input_file)


