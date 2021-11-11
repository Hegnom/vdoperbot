import mysql.connector
from varconf import * 
mydb = mysql.connector.connect(
  host=HOST,
  user=USERDB,
  password=DBPASS,
  database=DB
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE video (uid VARCHAR(8000), fileid VARCHAR(800), tags VARCHAR(800), fileuniqueid VARCHAR(800), userid VARCHAR(800))")