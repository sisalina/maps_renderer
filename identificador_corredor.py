import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math

for track_id in range(1684,1685):

	offset = 0

	try:

		# Conexion con la DB
		conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
		cur = conn.cursor()
		cur.execute("SELECT * FROM points WHERE track_id = '" + str(track_id) + "' ORDER BY id")
		rows = cur.fetchall()
		lat_ini = -32.931824
		lon_ini = -60.650254
		lat_fin = -32.954630
		lon_fin = -60.656047
		a = (lat_ini - lat_fin)/(lon_ini - lon_fin)
		b = lat_ini - a*lon_ini
		#print a
		#print b

		for row in rows:
			y = row[1] # lat
			x = row[2] # lon
			d = (a*x - y + b)/math.sqrt(a**2 + 1) 
			d = math.radians(abs(d))*6371*1000
			print str(x) + "," + str(y) + "," + str(d)
			#print "x= " + str(x) + ", y= " + str(y) + ", D= " + str(d)
			if d < 30:
				offset = offset + 1
			if offset >= 30:
				print track_id
				break


		# Actualiza la DB
		#frase = "UPDATE tracks SET origenlat = "+str(origen_lat)+", origenlon = "+str(origen_lon)+", destinolat = "+ str(destino_lat)+", destinolon = "+str(destino_lon)+", velocidad = "+str(round(vel,2))+", tiempo = "+str(delta)+", distancia = " +  str(round(distancia,2)) + " WHERE id = " + str(track_id)
		#cur.execute(frase)
		#conn.commit()
		cur.close()

	except:

		print "Fallo edicion track " + str(track_id)
