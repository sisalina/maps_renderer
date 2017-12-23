import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import operator
from shutil import copyfile
import os
import shutil
from time import sleep

original_out = "/home/sebas/Escritorio/BID/Listas_CSV/lista_publicos.csv"
copia_out    = "/home/sebas/Escritorio/BID/Listas_CSV/lista_publicos_copia_2.csv"

def copiar_archivo(copia_out, original_out):
	src = open(copia_out, 'rU') 
	dst = open(original_out, 'w') 
	for line in iter(src):
		dst.write(line)
	original.close()


# 1224,2495 Eleccion justificada segun viajes realizados
# 2600,7000 Eleccion arbitraria 

for track_id in range (2600,7000): 

	print "copiando track id = " + str(track_id)
	
	input    = "/home/sebas/Escritorio/BID/CSV_interpolados/track_" + str(track_id)  + ".csv"
	track    = open(input, 'rU') 
	original = open(original_out, 'rU') 
	copia    = open(copia_out, 'w') 

	buffer = original.readlines()

	a = 0

	for line in iter(track):

		comps = line.split(",")
		lat = comps[1]
		lon = comps[2].replace("\n","")

		# Busco linea archivo original
		try:
			linea  = buffer[a].replace("\n","")
			linea = str(linea) + lat + "," + lon + ";" + "\n"

			
		except:
			linea = lat + "," + lon + ";" + "\n"

		copia.write(linea)

		# Sumo contador
		a = a + 1
		
	# Sobrescribir copia sobre original 
	track.close()
	copia.close()
	copiar_archivo(copia_out, original_out)
