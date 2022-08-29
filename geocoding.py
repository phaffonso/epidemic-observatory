
import credentials_geo
import googlemaps
import storage_postgres as storage
import re

re1 = re.compile('(^| )(he|she|ele|ela|they|ella) ?[/\|\- ] ?(her|him|ella|el|they|them|dela|dele|a)', re.IGNORECASE)
re2 = re.compile('(where|world|planet|earth|mundo)', re.IGNORECASE)
re3 = re.compile('[0-9][0-9](\+|y)', re.IGNORECASE)
re4 = re.compile("[\(\+'][0-9]{2}\)?", re.IGNORECASE)
re5 = re.compile('bts|enhypen|heeseung', re.IGNORECASE)
re6 = re.compile('^[0-9]+$')

# geocode_result = gmaps.geocode('Mountain View, CA')
# print(geocode_result)
# print(storage.getUngeocodedLocations())

def isLocation(text):
    return (len(text) < 50 and
            re1.search(text) is None and
            re2.search(text) is None and
            re3.search(text) is None and
            re4.search(text) is None and
            re5.search(text) is None and
            re6.search(text) is None)

limit = 100

def geocodeAndSave():
    count = 0
    gmaps = googlemaps.Client(key=credentials_geo.API_KEY)
    for loc in storage.getUngeocodedLocations():
        if(isLocation(loc[0]) and storage.getGeocoded(loc[0]) is None):
            print(loc[0])
            geocode_result = gmaps.geocode(loc)
            print(geocode_result)
            storage.saveGeocoded(loc, geocode_result)
            count += 1
            print('---saved---')
            if(count >= limit):
              return

geocodeAndSave()
