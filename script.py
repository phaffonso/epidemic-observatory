import tweepy
import credentials
import sys
import json

# api = tweepy.API(credentials.BEARER_TOKEN)

# Set up words to track
keywords_to_track = ['febre, tosse, gripe']

try:
    with open('data.txt', x):
        x.write('[\r\n')
except:
    pass
    #ignore exception - will be thrown if file already exists

# Subclass Stream to print IDs of Tweets received
class MyStream(tweepy.Stream):

    #fields of interest that will be saved
    tweet_fields = ['text', 'created_at', 'geo', 'place', 'lang', 'retweeted']
    user_fields = ['id', 'geo_enabled', 'lang']

    def on_status(self, status):
        print('##STATUS')
        tweet = {}
        tweet['user'] = {}
        for field in self.tweet_fields:
            tweet[field] = str(status.__dict__[field])
        for field in self.user_fields:
            tweet['user'][field] = status.user.__dict__[field]
        with open('data.txt', 'a') as file:
            file.write(',\r\n')
            json.dump(tweet, file, indent=2)
        with open('rawdata.txt', 'a', encoding="utf-8") as file:
            file.write('\r\n>>>')
            file.write(str(status))
        print(tweet)
        sys.stdout.flush()

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
  credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET,
  credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET
)

# Begin collecting data
print("call filter")
my_stream.filter(track = keywords_to_track)
print("after filter")

# v2 api example
# client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN)
