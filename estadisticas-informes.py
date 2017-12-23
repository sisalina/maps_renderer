import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math

primer_punto  = [-32.96617,-60.62496]
segundo_punto = [-32.96657,-60.62391]
radio_máximo = 20 # metros

for track_id in range(2618,2619):
	conn = psycopg2.connect("dbname='mylocaldb' user='sebas' host='192.168.1.106' password='ilwys238'")
	cur = conn.cursor()
	cur.execute("SELECT * FROM points WHERE track_id = '" + str(track_id) + "' ORDER BY id")
	rows = cur.fetchall()
	for row in rows:
		lat = float(row[1])
		lon = float(row[2])
		diferencia = math.radians(math.sqrt(dif_lat**2 + dif_lon**2))*6371