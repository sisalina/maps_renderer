import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import operator

fecha = "'2016-02-23 20:49:24.320594'"
genero_int = 0

conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
cur = conn.cursor()

input  = "/home/sebas/Escritorio/BID/scripts/bases/genero_tracks.txt"
f      = open(input, 'rU')  
 
for line in iter(f):    
	track_id = str(line).replace("\n","").split(";")
	genero = track_id[1]
	track_id = track_id[0]
	if genero == "M":
		genero_int = "1"
	else:
		genero_int = "0"
			
	cur.execute("UPDATE tracks SET destino = "+  genero_int  + " WHERE id = " + str(track_id))
	conn.commit()

cur.close()