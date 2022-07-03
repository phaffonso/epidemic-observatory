
import credentials_geo
import googlemaps
import storage_postgres as storage
import re

re1 = re.compile('(^| )(he|she|ele|ela|they|ella) ?[/\|\- ] ?(her|him|ella|el|they|them|dela|dele|a)', re.IGNORECASE)
re2 = re.compile('(where|world|planet|earth|mundo)', re.IGNORECASE)
re3 = re.compile('[0-9][0-9](\+|y)', re.IGNORECASE)
re4 = re.compile('^\(?\+?[0-9]+\)?$', re.IGNORECASE)

# geocode_result = gmaps.geocode('Mountain View, CA')
# print(geocode_result)
# print(storage.getUngeocodedLocations())

def isLocation(text):
    return (len(text) < 50 and
            re1.match(text) is None and
            re2.match(text) is None and
            re3.match(text) is None and
            re4.match(text) is None)

def geocodeAndSave():
    gmaps = googlemaps.Client(key=credentials_geo.API_KEY)
    for loc in storage.getUngeocodedLocations():
        if(isLocation(loc[0]) and storage.getGeocoded(loc) is None):
            print(loc[0])
            geocode_result = gmaps.geocode(loc)
            print(geocode_result)
            storage.saveGeocoded(loc, geocode_result)
            print('---saved---')

geocodeAndSave()
