#connect to cospas-sarsat database
import mysql.connector
dbase='cospas_staging'
user='cospas'
portno=4000
pw='Sk!#9nJ%@h1'
hostip='localhost' #66.155.96.18'
cnx = mysql.connector.connect(user=user, password=pw, port=portno,
                              host=hostip,
                              database=dbase)

cursor = cnx.cursor()
#cursor.execute("USE "+dbase+';')
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()      
for (table_name,) in tables:
        print table_name

cnx.close()


