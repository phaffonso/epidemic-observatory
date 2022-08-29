import psycopg2
import credentials_db_postgres as credentials_db
import json

mydb = psycopg2.connect(
  host=credentials_db.HOST,
  user=credentials_db.USER,
  password=credentials_db.PASSWORD,
  database='epi'
)

mycursor = mydb.cursor()

def point2str(point):
    return '(%.6f,%.6f)' % (point[0], point[1])

def coords2str(coords):
    points = tuple(map(point2str, coords[0]))
    return "(%s,%s,%s,%s)" % (points)

def getPlace(id):
    sql = "Select id from place where id = %s"
    param = (id,)
    mycursor.execute(sql, param)
    return mycursor.fetchone()

def getLocations():
    sql = 'select user_location from tweet where user_location is not null limit 40'
    mycursor.execute(sql)
    return mycursor.fetchall()

def getGeocoded(name):
    sql = 'select * from geocoded where location_name = %s'
    param = (name,)
    mycursor.execute(sql, param)
    return mycursor.fetchone()

def getAllGeocoded():
    sql = "select location_name, raw_geo_data from geocoded where raw_geo_data::text != '[]'"
    mycursor.execute(sql)
    return mycursor.fetchall()

def saveGeocoded(name, data):
    sql = 'insert into geocoded(location_name, raw_geo_data) values (%s, %s)'
    val = (name, json.dumps(data))
    mycursor.execute(sql, val)
    mydb.commit()

def saveGeocoded2(name, data, country, state):
    sql = 'insert into geocoded(location_name, raw_geo_data, country, state) values (%s, %s, %s, %s)'
    val = (name, json.dumps(data), country, state)
    mycursor.execute(sql, val)
    mydb.commit()

def getUngeocodedLocations():
    sql = ('select t.user_location from tweet t '
            'left outer join geocoded g on t.user_location = g.location_name '
            'where t.user_location is not null '
            'and g.location_name is null '
            'group by t.user_location '
            'order by count(t.user_location) desc '
            'limit 20000')
    mycursor.execute(sql)
    return mycursor.fetchall()

def createPlace(place):
    sql = ("insert into place (id, url, place_type, name, full_name, country_name, country_code, bounding_box) "
            " values (%s, %s, %s, %s, %s, %s, %s, %s)")
    val = (place.id, place.url, place.place_type, place.name,
            place.full_name, place.country, place.country_code,
            coords2str(place.bounding_box.coordinates))
    mycursor.execute(sql, val)
    mydb.commit()

def createCollection(keywords):
    sql = ("insert into tweet_collection (started, keywords) "
            " values (CURRENT_TIMESTAMP, %s) returning id")
    val = (keywords,)
    mycursor.execute(sql, val)
    id = mycursor.fetchone()
    mydb.commit()
    return id

def finishCollection(id):
    sql = ("update tweet_collection set finished =  "
            " CURRENT_TIMESTAMP where id = %s")
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()

def save(tweet, collection_id):

    place_id = None
    if(tweet.place != None):
        print("##  PLACE  ##")
        place_id = tweet.place.id
        if (getPlace(place_id) == None):
            print("##  CREATE PLACE  ##")
            createPlace(tweet.place)

    sql = (
        "INSERT INTO tweet (text, created_at, lang, retweeted, is_quote, is_reply, "
        " user_id, user_lang, user_geo_enabled, user_location, coordinates, place_id, collection_id)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    val = (tweet.text, tweet.created_at, tweet.lang, tweet.retweeted, tweet.is_quote_status,
            False if (tweet.in_reply_to_status_id is None) else True,
            tweet.user.id, tweet.user.lang, tweet.user.geo_enabled, tweet.user.location,
            None if tweet.coordinates is None else str(tweet.coordinates),
            place_id, collection_id)
    #print(tweet.user)

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "tweet saved")

#coords = [[[-43.416139, -22.813278], [-43.416139, -22.475838], [-43.177605, -22.475838], [-43.177605, -22.813278]]]
#print(coords2str(coords))
