from droneapi.lib import VehicleMode
from droneapi.lib import Location     #necessaire ?
from pymavlink import mavutil
import time
import socket
from LesOutilsDeJuju.utilitaires import * 

api = local_connect()
v   = api.get_vehicles()[0]
print " droneapi get_vehicle started"

_WP_LOITER_RAD            = v.parameters['WP_LOITER_RAD']   # 80 pour le rascal
_direction_piste          = gps_bearing(43.233559,-0.104083,43.234261,-0.100722)  #74 degres
_location_arbre           = Location(43.23290, -0.10831, 0, is_relative=True)

(_lat,_lon)               = gps_newpos( _location_arbre.lat, _location_arbre.lon, _direction_piste + 90, _WP_LOITER_RAD)
_location_attente_mav0    = Location (_lat, _lon, 125, is_relative=True)

(_lat,_lon)               = gps_newpos( _location_attente_mav0.lat, _location_attente_mav0.lon, _direction_piste + 180, 2*3.14159*_WP_LOITER_RAD)
(_lat,_lon)               = gps_newpos( _lat, _lon, _direction_piste - 90, 10)
_location_attente_mav1    = Location (_lat, _lon, 125, is_relative=True)

_circle_theta0  = (_direction_piste - 90) % 360

# 2. SYNCHRONISATION : Vehicule esclace se syncrhonise sur le maitre en mode GUIDED
_swarm_server_addr    = ('127.0.0.1',14549)
_swarm_client1_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_swarm_client1_socket.bind(_swarm_server_addr)
print " socket UDP 14549 ouvert"

log_file = open('log_mav1sync.txt','a')
log_file.write("\n\nDebut synchronisation des avions  -- "+str(time.time()))
log_file.write("\n Temps\tdistance\tDelta_Speed\tcmd_TRIM_ARSPD_CM\tTRIM_ARSPD_CM")
log_file.close()

_last_time = time.time() 
while not api.exit:
    data, addr = _swarm_client1_socket.recvfrom(1024)
    _mav0_location = Location(float(str(data).split("=")[1].split(",")[0]), float(str(data).split("=")[2].split(",")[0]), float(str(data).split("=")[3].split(",")[0]), str(data).split("=")[4].split(",")[0] == 'True')
    if time.time() - _last_time > 4:
        _last_time = time.time()
        # distance angulaire entre les avions 
        _mav1_bearing = gps_bearing(_location_attente_mav1.lat, _location_attente_mav1.lon, v.location.lat, v.location.lon)
        _mav0_bearing = gps_bearing(_location_attente_mav0.lat, _location_attente_mav0.lon, _mav0_location.lat, _mav0_location.lon)
        _distance_angulaire = (_mav1_bearing - _mav0_bearing) % 360
        if _distance_angulaire > 180:  # conversion des angles en -180 +180
            _distance_angulaire -= 360 # negatif quand l'esclave est en retard 
        # distance en metres (positif quand l'esclave est en avance)
        _distance_curviligne = _distance_angulaire / 360 * 2 * 3.14159 * _WP_LOITER_RAD
        log_file = open('log_mav1sync.txt','a')
        log_file.write("\n" + str(time.time()))
        log_file.write("\t" + str(_distance_curviligne))
        _delta_vitesse =  -_distance_curviligne / 5
        log_file.write("\t"+str(_delta_vitesse))
        if _delta_vitesse > 10:
            _delta_vitesse = 10
        if _delta_vitesse < -10:
            _delta_vitesse = -10
        cmd_TRIM_ARSPD_CM = 2000+100*_delta_vitesse
        log_file.write("\t"+str(cmd_TRIM_ARSPD_CM))
        v.parameters['TRIM_ARSPD_CM']= int(cmd_TRIM_ARSPD_CM) #2200 par defaut pour le rascal
        v.flush()
        log_file.write("\t"+str(v.parameters['TRIM_ARSPD_CM']))
        log_file.close()
#        # passage en mode AUTO quand distance est OK
#        if vehicle.mode.name=='GUIDED' and abs(_distance_metres_surlecercle) < 3:
#            vehicle.mode = VehicleMode("AUTO")

print "Server Stopped"
_swarm_client1_socket.close()


# 3. PASSAGE : Vehicule esclave fait un passage
# realise la mission
# regule distance par la vitesse de l'esclave 
# retourne a la sequence 1 : ATTENTE
