import os

input  = "/home/sebas/Escritorio/Labs/GEOfiles_Ciudades/Bahia/tracks.txt"
f      = open(input, 'rU')

for line in iter(f):
    track_id = line.replace("\n","")
#    os.system("gpsbabel -i csv -f /home/sebas/Escritorio/BID/CSV/track_" + str(track_id)  + ".csv -o gpx -f /home/sebas/Escritorio/BID/GPX/track_" + str(track_id)  + ".gpx")
    frase = "ogr2ogr -append tracks_hombres_y_mujeres /home/sebas/Escritorio/DB/Rubiapp/Post-Bahia/GPX/track_" + str(track_id)  + ".gpx"
#    print frase
    os.system(frase)
