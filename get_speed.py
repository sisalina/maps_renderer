import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import operator

conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
cur = conn.cursor()
output0 = "/home/sebas/Escritorio/BID/CSV/velocidad_0.csv"
output1 = "/home/sebas/Escritorio/BID/CSV/velocidad_1.csv"
output2 = "/home/sebas/Escritorio/BID/CSV/velocidad_2.csv"
output3 = "/home/sebas/Escritorio/BID/CSV/velocidad_3.csv"
output4 = "/home/sebas/Escritorio/BID/CSV/velocidad_4.csv"
output4 = "/home/sebas/Escritorio/BID/CSV/velocidad.csv"
arch0 = open(output0, "w") ## Cambiar a CSV o NMEA
arch1 = open(output1, "w") ## Cambiar a CSV o NMEA
arch2 = open(output2, "w") ## Cambiar a CSV o NMEA
arch3 = open(output3, "w") ## Cambiar a CSV o NMEA
arch4 = open(output4, "w") ## Cambiar a CSV o NMEA
arch5 = open(output4, "w") ## Cambiar a CSV o NMEA
a = 0

# Escribe PSQL en CSV
arch0.write("lat,lon,date,speed" + '\n' )
arch1.write("lat,lon,date,speed" + '\n' )
arch2.write("lat,lon,date,speed" + '\n' )
arch3.write("lat,lon,date,speed" + '\n' )
arch4.write("lat,lon,date,speed" + '\n' )
arch5.write("lat,lon,date,speed" + '\n' )


for track_id in range (2603,4000): # 6200 

	cur.execute("SELECT * FROM points WHERE track_id = " + str(track_id) + " ORDER BY id ASC")
	rows = cur.fetchall()
	largo_track = len(rows)
	
	lat_ini = 0
	lon_ini = 0
	t_ini   = 0
	
	for puntos in range (1,largo_track):  

		a = a + 1
		dif_lat = float(rows[puntos][1]) - lat_ini
		dif_lon = float(rows[puntos][2]) - lon_ini
		t   	= str(rows[puntos][3]).split(":")
		t 		= int(t[0])*3600 + int(t[1])*60 + int(t[2])
		d   	= math.radians(math.sqrt(dif_lat**2 + dif_lon**2))*6371
		dif_t   = t - t_ini
		# Que no se calcule el mismo punto
		if dif_t != 0:
			v = d/dif_t*3600
				
		lat_ini = float(rows[puntos][1]) 
		lon_ini = float(rows[puntos][2])
		t_ini   = t

		# Filtro
		if  v <= 5 :
			frase = str(rows[puntos][1]) + ',' + str(rows[puntos][2]) + ',' + str(rows[puntos][3])  + ',' + str(v) + '\n'
			arch0.write(frase)

		if v > 5 and v <=  10:
			frase = str(rows[puntos][1]) + ',' + str(rows[puntos][2]) + ',' + str(rows[puntos][3])  + ',' + str(v) + '\n'
			arch1.write(frase)

		if v > 10 and v <= 15 :
			frase = str(rows[puntos][1]) + ',' + str(rows[puntos][2]) + ',' + str(rows[puntos][3])  + ',' + str(v) + '\n'
			arch2.write(frase)

		if v > 15 and v <= 20 :
			frase = str(rows[puntos][1]) + ',' + str(rows[puntos][2]) + ',' + str(rows[puntos][3])  + ',' + str(v) + '\n'
			arch3.write(frase)

		if v > 20:
			frase = str(rows[puntos][1]) + ',' + str(rows[puntos][2]) + ',' + str(rows[puntos][3])  + ',' + str(v) + '\n'
			arch4.write(frase)

		if v < 40 and a%10==0:
			frase = str(rows[puntos][1]) + ',' + str(rows[puntos][2]) + ',' + str(rows[puntos][3])  + ',' + str(v) + '\n'
			arch5.write(frase)


cur.close()
arch0.close()
arch1.close()
arch2.close()
arch3.close()
arch4.close()
print a