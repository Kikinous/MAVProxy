#!/usr/bin/env python
from LesOutilsDeJuju.utilitaires import *
from droneapi.lib import Location    

# Parametres 1.2 #######################################################################################################
_WP_LOITER_RAD            = 80                                                    # 80 pour le rascal
_direction_piste          = gps_bearing(43.233559,-0.104083,43.234261,-0.100722)  # 74 degres
_location_depart          = Location(43.23270, -0.10831, 0, is_relative=True)     # a l'intersection
_longueur_passage         = 500                                                   # metres

# Calculs 1.2 ##########################################################################################################
(_lat,_lon)               = gps_newpos( _location_depart.lat, _location_depart.lon, _direction_piste, 500)
_location_arrivee         = Location (_lat, _lon, 100, is_relative=True)

_location_depart_mav0     = _location_depart
(_lat,_lon)               = gps_newpos(_location_depart.lat,_location_depart.lon, _direction_piste + 90, _WP_LOITER_RAD)
_location_attente_mav0    = Location (_lat, _lon, 100, is_relative=True)
_location_arrivee_mav0    = _location_arrivee

#(_lat,_lon)               = gps_newpos( _location_depart_mav0.lat, _location_depart_mav0.lon, _direction_piste - 90, 10)
#_location_depart_mav1     = Location (_lat, _lon, 125, is_relative=True)
#(_lat,_lon)               = gps_newpos( _location_attente_mav0.lat, _location_attente_mav0.lon, _direction_piste + 180, 
#                                            2*3.14159*_WP_LOITER_RAD)
#(_lat,_lon)               = gps_newpos( _lat, _lon, _direction_piste - 90, 10)
#_location_attente_mav1    = Location (_lat, _lon, 125, is_relative=True)
#(_lat,_lon)               = gps_newpos(_location_arrivee_mav0.lat,_location_arrivee_mav0.lon, _direction_piste - 90, 10)
#_location_arrivee_mav1    = Location (_lat, _lon, 125, is_relative=True)

# Ecriture du fichier ##################################################################################################
file = open("mission_mav0.txt", "w")
file.write("QGC WPL 110\n")
file.write("0	0	0	16	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	1\n")
waypoints = [] # [(lat,lon)]
for x in xrange(0,11): # de 1 a 10
    waypoints.append( gps_newpos(_location_depart_mav0.lat,_location_depart_mav0.lon, _direction_piste, 
                                    x/10.0 * _longueur_passage))
    file.write("%s	0	3	16	0.000000	0.000000	0.000000	0.000000	%.6f	%.6f	125.000000	1\n" % (x,waypoints[x][0],waypoints[x][1]) )
file.close()
print "Fichier mission_mav0.txt a ete calcule"

