from droneapi.lib import VehicleMode
from droneapi.lib import Location
from pymavlink import mavutil
import time
import socket
from LesOutilsDeJuju.utilitaires import * 

api = local_connect()
v   = api.get_vehicles()[0]
print " droneapi get_vehicle started : esclave"


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

(_lat,_lon)               = gps_newpos( _location_depart_mav0.lat, _location_depart_mav0.lon, _direction_piste - 90, 10)
_location_depart_mav1     = Location (_lat, _lon, 125, is_relative=True)
(_lat,_lon)               = gps_newpos( _location_attente_mav0.lat, _location_attente_mav0.lon, _direction_piste + 180,
                                        2*3.14159*_WP_LOITER_RAD)
(_lat,_lon)               = gps_newpos( _lat, _lon, _direction_piste - 90, 10)
_location_attente_mav1    = Location (_lat, _lon, 125, is_relative=True)
(_lat,_lon)               = gps_newpos(_location_arrivee_mav0.lat,_location_arrivee_mav0.lon, _direction_piste - 90, 10)
_location_arrivee_mav1    = Location (_lat, _lon, 125, is_relative=True)

# 1. ATTENTE : 10m au dessus et un perimetre en arriere de l'arbre #####################################################
v.mode = VehicleMode("GUIDED")
v.commands.goto(_location_attente_mav1)
v.parameters['TRIM_ARSPD_CM']=2000  #2200 par defaut pour le rascal
v.parameters['SYSID_THISMAV']=2
v.flush()
print "TRIM_ARSPD_CM = "+str(v.parameters['TRIM_ARSPD_CM'])
print "SYSID_THISMAV = "+str(v.parameters['SYSID_THISMAV'])
