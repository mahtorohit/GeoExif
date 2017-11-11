import datetime
import json
import pickle
from pathlib import Path

url = "/Users/rohit/Downloads/Takeout/Location_History/Location_History.json"


class Location:
    latitude = None
    longitude = None
    date = None
    milisec = None
    accuracy = None


    def __init__(self, loc):
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
            if type(self.date) is not datetime.datetime:
                raise Exception("Invalid Data for creating Location object {} - {} - {}".format(self.lat, self.long, self.date))

        else:
            print(type(self.date))
            raise Exception("Invalid Data for creating Location object {} - {} - {}".format(self.lat, self.long, self.date))

    def __str__(self):
        return str("Time : {} - Latitude : {} - Longitude : {}".format(self.milisec,self.latitude,self.longitude))

    def __repr__(self):
        # return str("Date : {} - Latitude : {} - Longitude : {}".format(self.date.strftime('%Y-%m-%d'),self.latitude,self.longitude))
        return str("Time : {} - Latitude : {} - Longitude : {}".format(self.milisec, self.latitude, self.longitude))


class DataModel:
    path = None

    def __init__(self, path=url):
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
            loc_map = {}
            json_data = json_data["locations"]
            print(len(json_data))
            for i in range(len(json_data)):
                data.append(Location(json_data[i]))
                print("** i {}".format(i))
            pickle.dump(data, open("locations.p", "wb"))


    def load_data_map(self):
        with open(self.path) as data_file:
            json_data = json.load(data_file)
            data = []
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

                print("** i {} - {}".format(i,loc))

            pickle.dump(loc_map, open("/Users/rohit/Documents/Projects/GPSEXIF/com/gps/data/locations_map.p", "wb"))

    def get_location_map(self):
        with open("/Users/rohit/Documents/Projects/GPSEXIF/com/gps/data/locations_map.p", "rb") as input_file:
            return pickle.load(input_file)



    # def load_pickel_array(self):
    #     with open(r"locations_map.p", "rb") as input_file:
    #         json_data = pickle.load(input_file)
    #         # for i in range(100):
    #         #     l = json_data[i]
    #         #     print(l.date.strftime('%Y-%m-%d'))
    #         data = list(json_data.keys())
    #         for i in range(10):
    #             # l = json_data[i]
    #             print(data[i],json_data[data[i]])
    #
    # def load_pickel_map(self):
    #     with open(r"locations_map.p", "rb") as input_file:
    #         json_data = pickle.load(input_file)
    #         data = list(json_data.keys())
    #         for i in range(10):
    #             # l = json_data[i]
    #             print(data[i], len(json_data[data[i]]))
