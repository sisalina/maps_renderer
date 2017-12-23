import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import operator

def time_parts(time):
	t_h = time[0:2]
	t_m = time[3:5]
	t_s = time[6:8]
	t_abs = int(t_h)*3600 + int(t_m)*60 + int(t_s) 
	return t_abs

def write_csv(v_dia,track_id):
	target = open("/home/sebas/Escritorio/BID/CSV_interpolados/track_" + str(track_id)  + ".csv", "w")
	for secs in range (0,86400):  
		frase = str(secs) + ',' + str(v_dia[secs][0]) + ',' + str(v_dia[secs][1]) + '\n' 
		target.write(frase)
	target.close()

for track_id in range (2600,7000): # 2495 
	input = "/home/sebas/Escritorio/BID/CSV/track_" + str(track_id)  + ".csv"
	#num_lines = sum(1 for line in open(input))
	arch = open(input, 'rU') 

	w, h = 2, 86400 
	v_dia = [[0 for x in range(w)] for y in range(h)] 

	itercsv = iter(arch)
	next(itercsv)

	for line in iter(itercsv):  
		comps = line.split(",")
		buffer_lon = float(comps[0])
		buffer_lat = float(comps[1])
		buffer_t   = comps[2]
		t_abs = time_parts(buffer_t.replace("\n",""))
		v_dia[t_abs][0] = comps[0]
		v_dia[t_abs][1] = comps[1]
		break

	for line in iter(itercsv):  

		# parsing
		comps = line.split(",")
		lat = float(comps[0])
		lon = float(comps[1])
		t   = comps[2].replace("\n","")
		t_abs = time_parts(t) 

		# Process stage
		t_dif = t_abs - time_parts(buffer_t.replace("\n",""))

		if t_dif > 1000 or t_dif == 0:
			print "cambio de dia, track_id: " + str(track_id) 
		else:
			#print str(t_abs) + "," + str(lat) + "," + str(lon)
			lat_int_dif = (buffer_lat - lat)/t_dif
			lon_int_dif = (buffer_lon - lon)/t_dif

			# valores iterados
			for i in range (1, t_dif):
				v_dia[time_parts(buffer_t) + i][0] = lat + lat_int_dif*(i) # interpolacion latitud
				v_dia[time_parts(buffer_t) + i][1] = lon + lon_int_dif*(i) # interpolacion longitud
			# valors reales
			v_dia[t_abs][0] = lat
			v_dia[t_abs][1] = lon

			# Buffer stage
			buffer_lat = float(comps[0])
			buffer_lon = float(comps[1])
			buffer_t   = comps[2]

#	print v_dia
	write_csv(v_dia,track_id)
		
				
#		print line.replace("\n","")

