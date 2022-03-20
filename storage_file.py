import json
import sys

filename = 'data3.json'

#fields of interest that will be saved
tweet_fields = ['text', 'created_at', 'geo', 'lang', 'retweeted']
user_fields = ['id', 'geo_enabled', 'lang']

try:
    with open(filename, x):
        x.write('[\r\n')
        print("File created")
except:
    print("File already exists")
    #ignore exception - will be thrown if file already exists

def save(status):
    tweet = {}
    tweet['user'] = {}
    tweet['place'] = None
    for field in tweet_fields:
        tweet[field] = str(status.__dict__[field])
    for field in user_fields:
        tweet['user'][field] = status.user.__dict__[field]
    if(status.place != None):
        tweet['place'] = {}
        for key in status.place.__dict__.keys():
            tweet['place'][key] = str(status.place.__dict__[key])
        tweet['place']['bounding_box'] = status.place.bounding_box.__dict__

    with open(filename, 'a') as file:
        file.write(',\r\n')
        json.dump(tweet, file, indent=2)
        print('file write')

    print(tweet)
    sys.stdout.flush()
