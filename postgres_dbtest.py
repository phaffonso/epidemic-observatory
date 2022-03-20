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

connection.commit()
