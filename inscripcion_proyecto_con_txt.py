import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import operator

fecha = "'2016-02-23 20:49:24.320594'"
proyecto_id = str(64)



conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
cur = conn.cursor()

# Proyecto Target ID = 51

input  = "/home/sebas/Escritorio/Compartida/Agustin-Compartida/mariano.txt"
f      = open(input, 'rU')  
 
for line in iter(f):    
	track_id = str(line)
	cur.execute("SELECT * FROM tracks WHERE id = " + track_id)
	rows = cur.fetchall()
	if len(rows) != 0:
		cur.execute("INSERT INTO unions (proyecto_id,track_id,created_at,updated_at) VALUES (" + proyecto_id + ',' + track_id + "," + fecha + "," + fecha + ")")
		conn.commit()
cur.close()

