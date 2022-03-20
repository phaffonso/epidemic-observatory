import tweepy
import credentials_twitter
import credentials_db
import sys
import storage_postgres as storage

# api = tweepy.API(credentials.BEARER_TOKEN)

# Set up words to track
keywords_to_track = ['febre, tosse, gripe']

# Subclass Stream to print IDs of Tweets received
class MyStream(tweepy.Stream):

    def on_status(self, status):
        #print('##STATUS')
        #if(status.place != None or status.geo != None):
        storage.save(status)
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

    def on_error(self, status_code):
        print("error::"+status_code)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

# Initialize instance of the subclass
my_stream = MyStream(
  credentials_twitter.CONSUMER_KEY,
  credentials_twitter.CONSUMER_SECRET,
  credentials_twitter.ACCESS_TOKEN,
  credentials_twitter.ACCESS_TOKEN_SECRET
)

# Begin collecting data
print("call filter")
my_stream.filter(track = keywords_to_track)
print("after filter")

# v2 api example
# client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN)
