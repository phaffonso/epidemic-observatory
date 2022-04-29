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
    points = map(point2str, coords[0])
    cstring = '((%s, %s, %s, %s))' % tuple(points)
    return 'POLYGON(%s)' % cstring

coords = [[[-43.416139, -22.813278], [-43.416139, -22.475838], [-43.177605, -22.475838], [-43.177605, -22.813278]]]
print(coords2str(coords))

sql = 'insert into place (id, bounding_box) values (%s, ST_GeomFromText(%s))'
var = ('2', 'POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))')

mycursor.execute(sql, var)
mydb.commit()
