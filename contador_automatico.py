import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import operator

lat1,lon1 =  -32.94879464987211,-60.64026653766632

lat2,lon2 =  -32.94936634980389,-60.63748776912689

# Inicio de variables
contador_global = 0
punto_A = 0
punto_B = 0
tiempo_A = 0
tiempo_B = 0
speed_bucket = 0

# Conexiones
input = "/home/sebas/Escritorio/BID/scripts/lista-mapas-calor/dia_unico_publico.txt"
conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
cur = conn.cursor()
f = open(input,'rU')

# Ejecucion - main 
for line in iter(f): 

	contador_A = 0
	contador_B = 0

	track = line.replace("\n","")
	cur.execute("SELECT * FROM points WHERE track_id = " + str(track) + " ORDER BY id ASC")
	rows = cur.fetchall()

	# Revisar punto a punto que pertenece a cada track
	for row in rows:
		info = row
		lat_point = float(info[1])
		lon_point = float(info[2])
		time_point= info[3]
		dif_loc_1 = math.radians(math.sqrt((lat1 - lat_point)**2 + (lon1 - lon_point)**2))*6371000 
		dif_loc_2 = math.radians(math.sqrt((lat2 - lat_point)**2 + (lon2 - lon_point)**2))*6371000 
		
		if dif_loc_1 < 50:
			contador_A = contador_A + 1
			punto_A  = dif_loc_1
			tiempo_A = time_point

		if dif_loc_2 < 50:
			contador_B = contador_B + 1
			punto_B  = dif_loc_2
			tiempo_B = time_point

	if contador_A > 0 and contador_B > 0:
		contador_global = contador_global + 1
		dif_tiempo = abs(datetime.combine(date.today(), tiempo_B) - datetime.combine(date.today(), tiempo_A)).total_seconds()
		distancia  = math.radians(math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2))*6371 # En kilometros 
		velocidad  = distancia/float(dif_tiempo)*3600
		speed_bucket = speed_bucket + velocidad 

if contador_global != 0:
	print speed_bucket/contador_global
print contador_global


