import psycopg2
import datetime
from datetime import timedelta
import math

tolerancia_mins  = 15
coincidencias    = 0
tracks_por_valid = 0
error = 0

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
estaciones = [est1,est2,est3,est4,est5,est6,est7,est8,est9,est10,est11,est12,est13,est14,est15,est16,est17,est18,[0,0]]

for track_id in range(7871,8684): # Comienza en 2603

	try:
		conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
		cur = conn.cursor()
		cur.execute("SELECT tiempo FROM points WHERE track_id = '" + str(track_id) + "' ORDER BY id ASC LIMIT 1")
		rows_principio = cur.fetchall()
		cur.execute("SELECT tiempo FROM points WHERE track_id = '" + str(track_id) + "' ORDER BY id DESC LIMIT 1")
		rows_final = cur.fetchall()
		hora_inicio = rows_principio[0][0]
		hora_final  = rows_final[0][0]
		cur.execute("SELECT fecha FROM tracks WHERE id = " + str(track_id))
		rows_dia_principio = cur.fetchall()
		rows_dia_principio = rows_dia_principio[0][0]
		cur.execute("SELECT * FROM tracks WHERE id = " + str(track_id))
		info = cur.fetchall()
		
		lat_salida_dbrubi  = float(info[0][8])
		lon_salida_dbrubi  = float(info[0][9])
		lon_llegada_dbrubi = float(info[0][10])
		lat_llegada_dbrubi = float(info[0][11])
		distancia = float(info[0][6])

		if distancia < 1: # Si la distancia es menor a un kilometro, entonces me salto este loop
			continue

		tracks_por_valid = tracks_por_valid + 1

		if hora_final > hora_inicio: 

			fecha_termino_track = datetime.datetime.combine(rows_dia_principio, hora_final)
			fecha_inicio_track  = datetime.datetime.combine(rows_dia_principio, hora_inicio)
		
		else:

			fecha_termino_track = datetime.datetime.combine(rows_dia_principio + timedelta(days=+1), hora_final)
			fecha_inicio_track  = datetime.datetime.combine(rows_dia_principio, hora_inicio)

		correccion_gmt  = timedelta(hours=-3)

		fecha_busqueda_inicio = fecha_inicio_track + correccion_gmt
		fecha_busqueda_final  = fecha_termino_track + correccion_gmt


		input = "/home/sebas/Escritorio/BID/scripts/bases/info_emtr.txt"
		f = open(input,'rU')

		resultados = 0


		for line in iter(f): # Iteracion del archivo lista proporcionado por EMTR
			
			contenido_viaje = line
			componentes = contenido_viaje.split(";")
			fecha       = componentes[0] # 24/10/2016 23:54:19
			fecha_coms  = fecha.split(" ")
			fecha_date  = fecha_coms[0].replace('\xef\xbb\xbf\xef\xbb\xbf',"").split("-") # remover codificacion espanol a la primera linea
			fecha_time  = fecha_coms[1].split(":")
			# 3-10-2016 00:06;5971424;paulo jose evangelsita filho;Finalizada;446;LECTOR;0h 9min 22seg;17 - Distrito Centro;13 - Plaza Sarmiento;0.0
			fecha_db_inicio = datetime.datetime(int(fecha_date[2]),int(fecha_date[1]),int(fecha_date[0]),int(fecha_time[0]),int(fecha_time[1]),int(0))
			duracion    = componentes[6]	#0h 21min 23se
			duracion    = duracion.split(" ")
			duracion_hrs  = int(duracion[0].replace("h",""))
			duracion_mins = int(duracion[1].replace("min",""))
			duracion_segs = int(duracion[2].replace("seg",""))
			fecha_db_final  = fecha_db_inicio + timedelta(hours=+duracion_hrs, minutes=+duracion_mins, seconds=+duracion_segs)
			user_id 	= componentes[1]
			nombre  	= componentes[2]
			patente 	= componentes[4]
			estacion_i  = componentes[7]
			estacion_f  = componentes[8]
			estacion_i  = estacion_i.split("-")
			estacion_f  = estacion_f.split("-")
			estacion_i  = estacion_i[0]
			estacion_f  = estacion_f[0]
			if estacion_i == '' or estacion_f == '' or estacion_i == "901 " or estacion_f == "901 ":
				estacion_i  = 18 # Estacion falsa
				estacion_f  = 18 # Estacion falsa
				error = error + 1

			lat_salida  = estaciones[int(estacion_i)-1][0]
			lon_salida  = estaciones[int(estacion_i)-1][1]
			lat_llegada = estaciones[int(estacion_f)-1][0]
			lon_llegada = estaciones[int(estacion_f)-1][1]
			
			dif_lat_salida  = lat_salida - lat_salida_dbrubi
			dif_lon_salida  = lon_salida - lon_salida_dbrubi
			dif_lat_llegada = lat_llegada - lat_llegada_dbrubi
			dif_lon_llegada = lon_llegada - lon_llegada_dbrubi

			dif_salida  = math.radians(math.sqrt(dif_lat_salida**2 + dif_lon_salida**2))*6371000
			dif_llegada = math.radians(math.sqrt(dif_lat_llegada**2 + dif_lon_llegada**2))*6371000

			dif_fecha_inicio  = abs(fecha_busqueda_inicio - fecha_db_inicio).seconds
			dif_fecha_termino = abs(fecha_busqueda_final  - fecha_db_final).seconds

			if dif_fecha_inicio < 700 and dif_fecha_termino < 700 and dif_llegada < 1500 and dif_salida < 1500: 
	#		if dif_fecha_inicio < 300 and dif_fecha_termino < 300: 
				resultados = 1 + resultados



		if resultados > 1:
			coincidencias = coincidencias + 1		

		print str(track_id) + ";" + str(resultados)

	
	except:
		error = error + 1

print str(coincidencias) + '/' + str(tracks_por_valid)