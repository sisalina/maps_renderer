# Script Estadisticas - Modifica valores en DB 
# Calcula:
# 1. Distancia Recorrida
# 2. Tiempo Total
# 3. Velocidad Promedio
# 4. Origen (lat, lon)
# 5. Destino (lat, lon)

import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math

for track_id in range(8430,9000):

	try:

		print "Editando track " + str(track_id)
		# Conexion con la DB
		conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
		cur = conn.cursor()
		cur.execute("SELECT * FROM points WHERE track_id = '" + str(track_id) + "' ORDER BY id")
		rows = cur.fetchall()

		# Origen y Destino
		origen_lat  = rows[-1][1]
		origen_lon  = rows[-1][2]
		destino_lat = rows[0][1]
		destino_lon = rows[0][2]
		# Tiempo Total
		tiempo_f = str(rows[0][3])
		tiempo_0 = str(rows[-1][3])
		tiempo_0 = int(tiempo_0[0:2])*3600 + int(tiempo_0[3:5])*60 + int(tiempo_0[6:8])
		tiempo_f = int(tiempo_f[0:2])*3600 + int(tiempo_f[3:5])*60 + int(tiempo_f[6:8])
		delta = tiempo_0 - tiempo_f
		if delta < 0:
			delta = tiempo_0 + 24*3600 - tiempo_f
		# Distancia Recorrida
		distancia = 0

		lat_p = rows[0][1]
		lon_p = rows[0][2]


		for row in rows:
			dif_lat = row[1] - lat_p
			dif_lon = row[2] - lon_p
			d = math.radians(math.sqrt(dif_lat**2 + dif_lon**2))*6371
			distancia = distancia + d;	
			lat_p = row[1]
			lon_p = row[2]		
		
		# Velocidad Promedio
		vel = distancia/delta*3600

		# Actualiza la DB
		frase = "UPDATE tracks SET origenlat = "+str(origen_lat)+", origenlon = "+str(origen_lon)+", destinolat = "+ str(destino_lat)+", destinolon = "+str(destino_lon)+", velocidad = "+str(round(vel,2))+", tiempo = "+str(delta)+", distancia = " +  str(round(distancia,2)) + " WHERE id = " + str(track_id)
		cur.execute(frase)
		conn.commit()
		cur.close()

	except:

		print "Fallo edicion track " + str(track_id)
