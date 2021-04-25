import sys
import os
import wand
import gmplot
from wand.image import Image

# Get Google Maps Js API key to use
apikey = ''

# http://docs.wand-py.org/en/0.4.2/
def getexif(filename):
    # Get Exif data from file
    exif = {} #instantiate exif list
    with Image(filename=filename) as image:
        exif.update((k[5:], v) for k, v in image.metadata.items()
        if k.startswith('exif:'))
        return (exif)

def convert(num, ref):
    # Parse the longitude or latitude passed, and convert to decimal
    num_split = num.split(",")
    coord = []
    for num in num_split:
        num = num.lstrip()
        num_0 = num.split("/")
        numX = float(num_0[0])/float(num_0[1])
        coord.append(numX)
    d = coord[0]
    m = coord[1]
    s = coord[2]
    value = d + (m / 60.0) + (s / 3600.0)
    if ref == 'W':
        value = 0 - value
    if ref == 'S':
        value = 0 - value
    return(value)

latitude_list = []
longitude_list = []
Items = os.listdir(".")  #list all files in current directory & store them in Items
Items.sort() #sort list
for names in Items: #loop through each file in Items list
    if (names.endswith(".jpg"):
        exif = getexif(names)
        if "GPSLatitude" in exif.keys():
            #pull exif from current image
            print(exif)
            lat = exif['GPSLatitude'] #pull the latitude from the exif
            lat_ref = exif['GPSLatitudeRef'].strip()
            lon = exif['GPSLongitude']
            lon_ref = exif['GPSLongitudeRef'].strip()
            lat = convert(lat, lat_ref)
            lon = convert(lon, lon_ref)
            latitude_list.append(lat) #add the current file's latitude to a list
            longitude_list.append(lon) #add the current file's longitude to a list
        else:
            print("No GPS data in EXIF")
        gmap1 = gmplot.GoogleMapPlotter(51.5351944444, -0.148519444444, 7, apikey=apikey) #setting the initial view point & zoom level for the final map
        gmap1.scatter(latitude_list, longitude_list, '#FF0000', size=10) #adding points to mark each set of coordinates from the list
        gmap1.plot(latitude_list, longitude_list,  'cornflowerblue', edge_width = 3.5) #adding lines to connect each set of coordinates from the list
        gmap1.draw("./map.html") #save the final map to the specifieddirectory with the specified name
