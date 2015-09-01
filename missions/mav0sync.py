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

# Parametres 1.3 #######################################################################################################
_WP_LOITER_RAD            = v.parameters['WP_LOITER_RAD']                         # 80 pour le rascal
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
#                                        2*3.14159*_WP_LOITER_RAD)
#(_lat,_lon)               = gps_newpos( _lat, _lon, _direction_piste - 90, 10)
#_location_attente_mav1    = Location (_lat, _lon, 125, is_relative=True)
#(_lat,_lon)               = gps_newpos(_location_arrivee_mav0.lat,_location_arrivee_mav0.lon, _direction_piste - 90, 10)
#_location_arrivee_mav1    = Location (_lat, _lon, 125, is_relative=True)

# Adresses 1.0 #########################################################################################################
_mav1_server_addr     = ('127.0.0.1',14549) # recoit location de mav0
_mav0_client_addr     = ('127.0.0.1',14548) # emet   location de mav0
_mav0_server_addr     = ('127.0.0.1',14547) # recoit top synchronisation
_mav1_client_addr     = ('127.0.0.1',14546) # emet   top synchronisation

# 2. SYNCHRONISATION : le maitre envoie sa position ####################################################################
_mav0_client_socket   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_mav0_client_socket.bind(_mav0_client_addr)
print " socket UDP 14548 ouvert : envoie au port 15549"
_mav0_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_mav0_server_socket.bind(_mav0_server_addr)
print " socket UDP 14547 ouvert : reception de la syncrhonisation de mav1"


# attribute bserver callbacks 
def location_callback(attribute):
    _mav0_client_socket.sendto(str(v.location), _mav1_server_addr)

v.add_attribute_observer('location', location_callback)	

mav0_Etape = "SYNCHRONISATION"  # SYNCRHONISATION || RATTRAPAGE || PASSAGE
while not api.exit:

    if mav0_Etape == "SYNCHRONISATION" :
        data, addr = _mav0_server_socket.recvfrom(1024)
        #si top recut de mav1, alors passer a l'etape RATTRAPAGE
        if str(data) == "top_synchro":
            _bearing = gps_bearing(_location_attente_mav0.lat,_location_attente_mav0.lon, v.location.lat,v.location.lon)
            _bearing_topSynchro = _bearing
            mav0_Etape = "RATTRAPAGE"
            print "top_synchro recu a %s --> un tour puis passage" % _bearing_topSynchro

    # si etape rattrapage, faire un tour avant de passer en mode auto
    elif mav0_Etape == "RATTRAPAGE" :
        _bearing = gps_bearing(_location_attente_mav0.lat,_location_attente_mav0.lon, v.location.lat,v.location.lon)
        #print "angle parcouru = %s " % ((_bearing - _bearing_topSynchro)%360)
        if (_bearing - _bearing_topSynchro)%360 > 345 :
            v.mode = VehicleMode("AUTO")
            mav0_Etape = "PASSAGE"
            print "passage en mode AUTO a %s" % _bearing

    elif mav0_Etape == "PASSAGE" :
        _chemin_mav0 = gps_distance( _location_depart_mav0.lat, _location_depart_mav0.lon, v.location.lat, v.location.lon )
        if _chemin_mav0 > _longueur_passage :
            mav1_Etape = "FIN"
            v.mode = VehicleMode("GUIDED")
            v.commands.goto(_location_attente_mav0)
            v.flush()
            print "passage a l'etape FIN --> mode guided"

    elif mav1_Etape == "FIN" :    
        v.remove_attribute_observer('location', location_callback)	
        pass


print " Fermeture du socket et de l'observer"
v.remove_attribute_observer('location', location_callback)	
_mav0_client_socket.close()
_mav0_server_socket.close()
