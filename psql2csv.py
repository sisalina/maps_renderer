import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import operator

conn = psycopg2.connect("dbname='bahia' user='postgres' host='localhost' password='sebas'")
cur = conn.cursor()

for track_id in range (1,14169): # 2495

	cur.execute("SELECT * FROM points WHERE track_id = " + str(track_id) + " ORDER BY id ASC")
	rows = cur.fetchall()
	arch = open("/home/sebas/Escritorio/DB/Rubiapp/Post-Bahia/CSV/track_" + str(track_id)  + ".txt", "w") ## Cambiar a CSV o NMEA
	largo_track = len(rows)
#
	# Escribe PSQL en CSV
#	arch.write("lat,lon,date" + '\n' )
##	for puntos in range (1,largo_track):
#		frase = str(rows[puntos][1]) + ',' + str(rows[puntos][2]) + ',' + str(rows[puntos][3]) + '\n'
#		arch.write(frase)
#	arch.close()

    # Escribe PSQL en NMEA
	# $GPRMC,135827.962,A,3326.0222,S,07035.8694,W,8.64,253.82,110115,,*0E

	#$GPRMC,135922.327,A,3326.0424,S,07035.9721,W,3.45,209.92,110115,,*09


	for puntos in range (1,largo_track):
		lat = rows[largo_track - puntos][1]*-1
		lat_int = int(lat)*100
		lat_dec = (lat - int(lat))*60
		lat_nmea = lat_int + lat_dec
		lon = rows[largo_track - puntos][2]*-1
		lon_int = int(lon)*100
		lon_dec = (lon - int(lon))*60
		lon_nmea = lon_int + lon_dec
		time = str(rows[largo_track - puntos][3])
		frase_pre = str("GPRMC," + time[0:2] + time[3:5]+ time[6:8] + ".123,A," + str(lat_nmea) + ",S,0" + str(lon_nmea) + ",W,0,0,110115,,")
		csum = 0
		for c in frase_pre:
			csum ^= ord(c)
		frase = "$GPRMC," + time[0:2] + time[3:5]+ time[6:8] + ".123,A," + str(lat_nmea) + ",S,0" + str(lon_nmea) + ",W,0,0,110115,,*" + str(csum)+ '\n'
		arch.write(frase)

	arch.close()


cur.close()
