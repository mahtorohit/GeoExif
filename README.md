# GeoExif
Add geo tag to images from imported google Map takeout JSON

Application overview:
![Application overviewt](https://github.com/mahtorohit/GeoExif/blob/master/app.png "Application overview")


# How to Use

Basic useful feature list:

 * Load JSON: Select google location takeout JSON file
 * Load Image Folder: Select Image folder which needs to be geotagged
 * Select location time Accuracy: Select time difference tolerance if location found for the image
 * Select Location time priority :
 	Past: location will search only past time stamp compare to Image timestamp
    Future: location will search only past time stamp compare to Image timestamp
    Any: Will select any closest location
 * Select Location overwrite policy :
 	OverWrite: Will overwrite current location
    Skip: Will Skip any operation if location already exist
 * Operation Type :
 	Search: Will only search for changes & show the count of effecting files
    Execute: Will make changes according to above-selected criteria