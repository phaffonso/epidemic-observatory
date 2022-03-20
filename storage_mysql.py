import mysql.connector
import credentials_db

mydb = mysql.connector.connect(
  host=credentials_db.HOST,
  user=credentials_db.USER,
  password=credentials_db.PASSWORD,
  database='default_schema'
)

mycursor = mydb.cursor()

def point2str(point):
    return '%.6f %.6f' % (point[0], point[1])

def coords2str(coords):
    points = tuple(map(point2str, coords[0]))
    return 'POLYGON((%s, %s, %s, %s, %s))' % (points + (points[0],))

def getPlace(id):
    sql = "Select id from place where id = %s"
    param = (id,)
    mycursor.execute(sql, param)
    return mycursor.fetchone()

def createPlace(place):
    sql = ("insert into place (id, url, place_type, name, full_name, country_name, country_code, bounding_box) "
            " values (%s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s))")
    val = (place.id, place.url, place.place_type, place.name,
            place.full_name, place.country, place.country_code,
            coords2str(place.bounding_box.coordinates))
    print('++', coords2str(place.bounding_box.coordinates))
    mycursor.execute(sql, val)
    mydb.commit()

def save(tweet):

    place_id = None
    if(tweet.place != None):
        print("##  PLACE  ##")
        place_id = tweet.place.id
        if (getPlace(place_id) == None):
            createPlace(tweet.place)

    sql = (
        "INSERT INTO tweet (text, created_at, lang, retweeted, user_id, user_lang, user_geo_enabled, coordinates, place_id)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    val = (tweet.text, tweet.created_at, tweet.lang, tweet.retweeted,
            tweet.user.id, tweet.user.lang, tweet.user.geo_enabled,
            None if tweet.coordinates is None else str(tweet.coordinates),
            place_id)

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
