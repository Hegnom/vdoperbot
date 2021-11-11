
import mysql.connector.pooling
from varconf import *


vdo_result=list()
connection_pool =  mysql.connector.pooling.MySQLConnectionPool(pool_name="mydb_pool",
                                                  pool_size=5,   
                                                  host=HOST,
                                                  pool_reset_session=False,
                                                  database=DB,
                                                  user=USERDB,
                                                  password=DBPASS)

class db:
    def video_fetch():
        global vdo_result
        with connection_pool.get_connection() as connection_object:
            with connection_object.cursor()as mycursor :
                mycursor.execute("SELECT uid, fileid ,tags ,fileuniqueid FROM video WHERE status ='True'")
                vdo_result.extend(mycursor.fetchall())
    def insert_vdo(val):
        with connection_pool.get_connection() as connection_object:
            with connection_object.cursor()as mycursor :
                sql = "INSERT INTO video (uid,fileid , fileuniqueid , tags , status, userid ) VALUES (%s, %s, %s, %s, %s,%s )"
                mycursor.execute(sql, val)
                connection_object.commit()
    def verify_updater(mod,value):
        with connection_pool.get_connection() as connection_object:
            with connection_object.cursor()as mycursor :
                if mod == 1:  
                    sql = 'UPDATE video SET status = "True" WHERE fileuniqueid = "%s" AND status ="False"'%value 
                if mod == 2 :
                    sql = 'DELETE FROM video WHERE status ="False" AND fileuniqueid="%s"'%value
                mycursor.execute(sql)
                connection_object.commit()
    def fetch_user_and_fileid(val):
        with connection_pool.get_connection() as connection_object:
            with connection_object.cursor()as mycursor :
                sql = 'SELECT uid , fileid, tags, fileuniqueid, userid FROM video WHERE  status= "False" AND fileuniqueid ="%s"'%val
                mycursor.execute(sql)
                myresult = mycursor.fetchone()   
                return myresult
