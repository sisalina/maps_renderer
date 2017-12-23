# Script Estadisticas - Modifica valores en DB 
# OUTPUT:
# 1. Recorridos que salen y llegan a X, Y estacion

import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math

est1  = [-32.95389, -60.65584]
est2  = [-32.95648, -60.64435]
est3  = [-32.95807, -60.63659]
est4  = [-32.95914, -60.62927]
est5  = [-32.96674, -60.62386]
est6  = [-32.96847, -60.62409]
est7  = [-32.93941, -60.6705]
est8  = [-32.94039, -60.66528]
est9  = [-32.94568, -60.65805]
est10 = [-32.94983, -60.65482]
est11 = [-32.94413, -60.65058]
est12 = [-32.94517, -60.6444]
est13 = [-32.94865, -60.64175]
est14 = [-32.94935, -60.63749]
est15 = [-32.94714, -60.63283]
est16 = [-32.9365, -60.65155]
est17 = [-32.93575, -60.64278]
est18 = [-32.94066, -60.63511]
vector_est = [est1,est2,est3,est4,est5,est6,est7,est8,est9,est10,est11,est12,est13,est14,est15,est16,est17,est18]

a_mistakes = 0

for track_id in range(2618,2620):

	try:
		# Conexion con la DB
		conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
		cur = conn.cursor()
		cur.execute("SELECT * FROM tracks WHERE id = '" + str(track_id) + "' ORDER BY id")
		rows = cur.fetchall()
		
		for row in rows:
		
			lat_salida  = row[8] 
			lon_salida  = row[9]
			lon_llegada = row[10] 
			lat_llegada = row[11]

			exito = 0

			for est_salida in range(0,18):
				
				for est_llegada in range(0,18):

					lat_est_salida  = vector_est[est_salida][0]
					lon_est_salida  = vector_est[est_salida][1]

					lat_est_llegada = vector_est[est_llegada][0]
					lon_est_llegada = vector_est[est_llegada][1]

					dif_lat  = lat_salida - lat_est_salida
					dif_lon  = lon_salida - lon_est_salida
					dif_lat2 = lat_llegada - lat_est_llegada
					dif_lon2 = lon_llegada - lon_est_llegada

					dif_salida  = math.radians(math.sqrt(dif_lat**2 + dif_lon**2))*6371000
					dif_llegada = math.radians(math.sqrt(dif_lat2**2 + dif_lon2**2))*6371000


					if dif_salida < 1000 and dif_llegada < 1000:
						print str(track_id) + "; salida = " + str(est_salida + 1) + ";salida = " + str(est_llegada + 1)
						exito = 1
					
			if exito == 0:

				print str(track_id) + "; no encontrado "

	except:
		a_mistakes = a_mistakes + 1
