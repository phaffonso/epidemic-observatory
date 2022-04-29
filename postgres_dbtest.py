import psycopg2
import credentials_db_postgres as credentials

connection = psycopg2.connect(
  host=credentials.HOST,
  user=credentials.USER,
  password=credentials.PASSWORD,
  database='epi'
)

mycursor = connection.cursor()
coords = [[[-43.416139, -22.813278], [-43.416139, -22.475838], [-43.177605, -22.475838], [-43.177605, -22.813278]]]

mycursor.execute('select * from country')
recset = mycursor.fetchall()
for rec in recset:
    print (rec)

def point2str(point):
    return '(%.6f,%.6f)' % (point[0], point[1])

def coords2str(coords):
    points = tuple(map(point2str, coords[0]))
    return "(%s,%s,%s,%s)" % (points)



sql = ("insert into place (id, bounding_box) values (%s,%s)")
val=('abcd', coords2str(coords))
mycursor.execute(sql, val)

connection.commit()
