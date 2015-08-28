from droneapi.lib import VehicleMode
from droneapi.lib import Location
from pymavlink import mavutil
import time
import socket
from LesOutilsDeJuju.utilitaires import * 

api = local_connect()
v   = api.get_vehicles()[0]
print " droneapi get_vehicle started : esclave"

_WP_LOITER_RAD            = v.parameters['WP_LOITER_RAD']   # 80 pour le rascal
_direction_piste          = gps_bearing(43.233559,-0.104083,43.234261,-0.100722)  #74 degres
_location_arbre           = Location(43.23290, -0.10831, 0, is_relative=True)

(_lat,_lon)               = gps_newpos( _location_arbre.lat, _location_arbre.lon, _direction_piste + 90, _WP_LOITER_RAD)
_location_attente_mav0    = Location (_lat, _lon, 125, is_relative=True)

(_lat,_lon)               = gps_newpos( _location_attente_mav0.lat, _location_attente_mav0.lon, _direction_piste + 180, 2*3.14159*_WP_LOITER_RAD)
(_lat,_lon)               = gps_newpos( _lat, _lon, _direction_piste - 90, 10)
_location_attente_mav1    = Location (_lat, _lon, 125, is_relative=True)


# 1. ATTENTE : arbre, un perimetre derriere, 10 m decalle
v.mode = VehicleMode("GUIDED")
v.commands.goto(_location_attente_mav1)
v.parameters['TRIM_ARSPD_CM']=2000  #2200 par defaut pour le rascal
v.parameters['SYSID_THISMAV']=2
v.flush()
print "TRIM_ARSPD_CM = "+str(v.parameters['TRIM_ARSPD_CM'])
print "SYSID_THISMAV = "+str(v.parameters['SYSID_THISMAV'])
