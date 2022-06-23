
import credentials_geo
import googlemaps
import storage_postgres as storage

gmaps = googlemaps.Client(key=credentials_geo.API_KEY)

# geocode_result = gmaps.geocode('Mountain View, CA')
# print(geocode_result)
# print(storage.getUngeocodedLocations())

for loc in storage.getUngeocodedLocations():
    if(storage.getGeocoded(loc) is None):
        print(loc)
        geocode_result = gmaps.geocode(loc)
        print(geocode_result)
        storage.saveGeocoded(loc, geocode_result)
        print('---saved---')
