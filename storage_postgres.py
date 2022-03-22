import psycopg2
import credentials_db_postgres as credentials_db

mydb = psycopg2.connect(
  host=credentials_db.HOST,
  user=credentials_db.USER,
  password=credentials_db.PASSWORD,
  database='epi'
)

mycursor = mydb.cursor()

def getPlace(id):
    sql = "Select id from place where id = %s"
    param = (id,)
    mycursor.execute(sql, param)
    return mycursor.fetchone()

def createPlace(place):
    sql = ("insert into place (id, url, place_type, name, full_name, country_name, country_code) "
            " values (%s, %s, %s, %s, %s, %s, %s)")
    val = (place.id, place.url, place.place_type, place.name,
            place.full_name, place.country, place.country_code)
    mycursor.execute(sql, val)
    mydb.commit

def createCollection():
    sql = ("insert into tweet_collection (started) "
            " values (CURRENT_TIMESTAMP) returning id")
    mycursor.execute(sql)
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
            createPlace(tweet.place)

    sql = (
        "INSERT INTO tweet (text, created_at, lang, retweeted, "
        " user_id, user_lang, user_geo_enabled, user_location, coordinates, place_id, collection_id)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    val = (tweet.text, tweet.created_at, tweet.lang, tweet.retweeted,
            tweet.user.id, tweet.user.lang, tweet.user.geo_enabled, tweet.user.location,
            None if tweet.coordinates is None else str(tweet.coordinates),
            place_id, collection_id)

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
