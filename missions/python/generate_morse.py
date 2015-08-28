#!/usr/bin/env python

from LesOutilsDeJuju.utilitaires import gps_newpos 
from LesOutilsDeJuju.utilitaires import gps_bearing 
from LesOutilsDeJuju.utilitaires import gps_distance 
  
distance  = gps_distance(43.234261,-0.100722,43.233559,-0.104083)
direction = gps_bearing(43.234261,-0.100722,43.233559,-0.104083)
direction_piste = direction-180
(lat,lon) = gps_newpos(43.234261,-0.100722,direction,distance/2.0)
print "direction de la piste West-Est = %s deg" % direction_piste

file = open("newfile.txt", "w")
file.write("QGC WPL 110\n")
file.write("0	0	0	16	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	1\n")
file.write("1	0	3	22	10.000000	0.000000	0.000000	0.000000	43.233385	-0.104455	35.00000	1\n")
file.write("2	0	3	16	0.000000	0.000000	0.000000	0.000000	43.233541	-0.108189	40.00000	1\n")

(lat,lon)=([43.233635],[-0.1074815])
for x in xrange(1,10):
    (lat_tmp,lon_tmp) = gps_newpos(lat[0],lon[0],direction_piste,x*50)
    lat.append(lat_tmp)
    lon.append(lon_tmp)
    file.write("%s	0	3	16	0.000000	0.000000	0.000000	0.000000	%s	%s	50.00000	1\n" % (x+2,lat[x],lon[x]) )

# ATTERRISSAGE par le nord
file.write("12	0	3	16	0.000000	0.000000	0.000000	0.000000	43.234730	-0.104552	40.000000	1\n")
file.write("13	0	3	16	0.000000	0.000000	0.000000	0.000000	43.235638	-0.099939	40.000000	1\n")
file.write("14	0	3	16	0.000000	0.000000	0.000000	0.000000	43.234722	-0.100036	40.000000	1\n")
file.write("15	0	3	16	0.000000	0.000000	0.000000	0.000000	43.234261	-0.100722	40.000000	1\n")
file.write("16	0	3	21	0.000000	0.000000	0.000000	0.000000	43.233559	-0.104083	3.000000	1\n")
