import datetime, time
import time
import select
import psycopg2
from datetime import date
from datetime import datetime, date
import math
import os


for track_id in range (1,14169):

#	os.system("gpsbabel -i csv -f /home/sebas/Escritorio/BID/CSV/track_" + str(track_id)  + ".csv -o gpx -f /home/sebas/Escritorio/BID/GPX/track_" + str(track_id)  + ".gpx")
	os.system("gpsbabel -i nmea -f /home/sebas/Escritorio/DB/Rubiapp/Post-Bahia/CSV/track_" + str(track_id)  + ".txt -x discard,hdop=10 -o gpx -F /home/sebas/Escritorio/DB/Rubiapp/Post-Bahia/GPX/track_" + str(track_id)  + ".gpx")
