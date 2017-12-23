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

user_id = 72
nombre = "Bici 007"
rubi_id = "BID2016-samp099"

# Conexion con la DB
conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
cur = conn.cursor()

for rubi in range(100,155):

	nombre = "Bici " + str(rubi)
	rubi_id = "BID2016-samp" + str(rubi)
	frase = "INSERT INTO rubis (user_id,nombre,identificacion,created_at,updated_at) VALUES (" + str(user_id) + ",'" + nombre + "','" +  rubi_id + "','2016-10-02 06:46:52','2016-10-02 06:46:52')"
	#frase = "DELETE FROM rubis WHERE id > 227 AND id < 338"
	print frase
	cur.execute(frase)
	conn.commit()


cur.close()