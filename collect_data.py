import tweepy
import credentials_twitter
import credentials_db
import sys
import storage_postgres as storage

import credentials_geo
import googlemaps

gmaps = googlemaps.Client(key=credentials_geo.API_KEY)

# api = tweepy.API(credentials.BEARER_TOKEN)

# Set up words to track
keywords_to_track = ['febre, tosse, gripe']

# Subclass Stream to print IDs of Tweets received
class MyStream(tweepy.Stream):

    def on_status(self, status):
        #print('##STATUS')
        #if(status.place != None or status.geo != None):
        global collection_id
        storage.save(status, collection_id)
        loc = status.user.location
        if(loc is not None):
            print("location: "+loc)
            if(storage.getGeocoded(loc) is None):
                print("geocoding: ")
                geocode_result = gmaps.geocode(loc)
                print(geocode_result)
                storage.saveGeocoded(loc, geocode_result)
            # with open('rawdata.txt', 'a', encoding="utf-8") as file:
            #     file.write('\r\n>>>')
            #     file.write(str(status))

    # def on_data(self, data):
    #     print("###DATA###")
    #     print(data.text)
    #     sys.stdout.flush()

    def on_close(self):
        print("closed")
        sys.stdout.flush()

    def on_closed(self):
        print("error: closed")

    def on_connection_error(self):
        print("error: connection err")

    def on_request_error(self):
        print("error: request err")

    def on_error(self, status_code):
        print("error::"+status_code)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

def main():
    # Initialize instance of the subclass
    my_stream = MyStream(
      credentials_twitter.CONSUMER_KEY,
      credentials_twitter.CONSUMER_SECRET,
      credentials_twitter.ACCESS_TOKEN,
      credentials_twitter.ACCESS_TOKEN_SECRET
    )

    # Begin collecting data
    print("call filter")
    global collection_id
    collection_id = storage.createCollection(keywords_to_track);
    print("tweet collection id %d" % collection_id)
    my_stream.filter(track = keywords_to_track)
    print("after filter")

    # v2 api example
    # client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN)

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("kbd interrupt")
        storage.finishCollection(collection_id)
        print("finished collection id %d" % collection_id)
    except SystemExit:
        print("system exit")
