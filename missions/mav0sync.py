from droneapi.lib import VehicleMode
from droneapi.lib import Location
from pymavlink import mavutil
import time
import socket
from LesOutilsDeJuju.utilitaires import * 
# Usage:
# - module load api
# - api start / stop / list

api = local_connect()
v = api.get_vehicles()[0]
print " droneapi get_vehicle started"

_WP_LOITER_RAD         = v.parameters['WP_LOITER_RAD']   # 80 pour le rascal
_direction_piste       = gps_bearing(43.233559,-0.104083,43.234261,-0.100722)  #74 degres
_location_arbre        = Location(43.23290, -0.10831, 0, is_relative=True)

(_lat,_lon)            = gps_newpos( _location_arbre.lat, _location_arbre.lon, _direction_piste + 90, _WP_LOITER_RAD)
_location_attente_mav0 = Location (_lat, _lon, 125, is_relative=True)

# 2. SYNCHRONISATION des MAV
_swarm_client_addr     = ('127.0.0.1',14548)
_swarm_server1_addr      = ('127.0.0.1',14549)
_swarm_client_socket   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_swarm_client_socket.bind(_swarm_client_addr)
print " socket UDP 14548 ouvert : envoie au port 15549"

# attribute bserver callbacks 
def location_callback(attribute):
    _swarm_client_socket.sendto(str(v.location), _swarm_server1_addr)

v.add_attribute_observer('location', location_callback)	

while not api.exit:
    _tmp=0

print " Fermeture du socket et de l'observer"
v.remove_attribute_observer('location', location_callback)	
_swarm_client_socket.close()
