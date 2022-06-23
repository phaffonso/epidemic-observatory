# Script que coleta dados (tweets) de rede social (Tweeter) relacionados a
# uma lista de palavras-chave de interesse especificadas e salva em banco de
# dados (padrão: PostgreSQL). Também pode realizar geocoding da localização do usuário
# usando API Google Maps, quando configurado para tal

import tweepy
import credentials_twitter
import credentials_db
import sys
import storage_postgres as storage

import credentials_geo
import googlemaps

gmaps = googlemaps.Client(key=credentials_geo.API_KEY)

########### PARÂMETROS AJUSTÁVEIS ############
# Palavras-chave de interesse na rede social
# keywords_to_track = ['febre, tosse, gripe']
keywords_to_track = ['febre, fever, fieber, fièvre, fiebre, حُمى, 发烧, 發燒, 熱, बुखार, netsu, demam, koorts, 열, yeol, ไข้, K̄hị']
# pt, en, de, fr, es, ar, jp, chn, hindi, indonesio, holandes, ko2, turco2
# Fazer ou não geocoding da localização de usuários - consome créditos do google maps API
# cujo custo pode varias entre 100-1000 reais por dia (alguns centavos por chamada)
use_geocoding = False

class MyStream(tweepy.Stream):

    def __init__(self, ck, cs, at, ats):
        self.collection_id = None
        super().__init__(ck, cs, at, ats)

    def on_status(self, status):
        #print('##STATUS')
        storage.save(status, self.collection_id)
        loc = status.user.location
        if(loc is not None):
            print("location: "+loc)
            if(use_geocoding and storage.getGeocoded(loc) is None):
                print("geocoding: ")
                try:
                    geocode_result = gmaps.geocode(loc)
                    print(geocode_result)
                    storage.saveGeocoded(loc, geocode_result)
                except:
                    print("An error occured while trying to geocode")
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

    def on_request_error(self, status_code):
        print("error: request err - code "+status_code)

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
    my_stream.collection_id = storage.createCollection(keywords_to_track);
    print("tweet collection id %d" % my_stream.collection_id)
    global collection_id
    collection_id = my_stream.collection_id
    my_stream.filter(track = keywords_to_track)
    print("after filter")

    # v2 api example
    # client = tweepy.Client(bearer_token=credentials.BEARER_TOKEN)

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("kbd interrupt")
        global collection_id
        storage.finishCollection(collection_id)
        print("finished collection id %d" % collection_id)
    except SystemExit:
        print("system exit")
