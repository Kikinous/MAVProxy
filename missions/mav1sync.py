from droneapi.lib import VehicleMode
from droneapi.lib import Location
from pymavlink import mavutil
import time
import socket
from LesOutilsDeJuju.utilitaires import * 

api = local_connect()
v   = api.get_vehicles()[0]
print " droneapi get_vehicle started"

# Parametres 1.3 #######################################################################################################
_WP_LOITER_RAD            = v.parameters['WP_LOITER_RAD']                         # 80 pour le rascal
_direction_piste          = gps_bearing(43.233559,-0.104083,43.234261,-0.100722)  # 74 degres
_location_depart          = Location(43.23270, -0.10831, 0, is_relative=True)     # a l'intersection
_longueur_passage         = 500                                                   # metres

# Calculs 1.3 ##########################################################################################################
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
_location_tengente_mav1   = Location (_lat, _lon, 125, is_relative=True)
(_lat,_lon)               = gps_newpos( _lat, _lon, _direction_piste - 90, 10)
_location_attente_mav1    = Location (_lat, _lon, 125, is_relative=True)
(_lat,_lon)               = gps_newpos(_location_arrivee_mav0.lat,_location_arrivee_mav0.lon, _direction_piste - 90, 10)
_location_arrivee_mav1    = Location (_lat, _lon, 125, is_relative=True)

# Adresses 1.0 #########################################################################################################
_mav1_server_addr     = ('127.0.0.1',14549)
_mav0_client_addr     = ('127.0.0.1',14548)
_mav0_server_addr     = ('127.0.0.1',14547)
_mav1_client_addr     = ('127.0.0.1',14546)

# 2. SYNCHRONISATION : esclace rattrape le maitre  #####################################################################
_mav1_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_mav1_server_socket.bind(_mav1_server_addr)
print " socket UDP 14549 ouvert : reception location mav0"
_mav1_client_socket   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_mav1_client_socket.bind(_mav1_client_addr)
print " socket UDP 14546 ouvert : envoie au port 15547 que mav1 est synchronise sur mav0"

log_file = open('log_mav1sync.txt','a')
log_file.write("\n\nDebut synchronisation des avions  -- "+str(time.time()))
log_file.write("\nTemps\tdistance\tDelta_Speed\tcmd_TRIM_ARSPD_CM\tTRIM_ARSPD_CM")
log_file.close()
print ""

mav1_Etape = "SYNCHRONISATION"  # SYNCRHONISATION || RATTRAPAGE || PASSAGE || FIN
_last_time = time.time() 
while not api.exit:
    data, addr = _mav1_server_socket.recvfrom(1024)
    _mav0_location = Location(float(str(data).split("=")[1].split(",")[0]),float(str(data).split("=")[2].split(",")[0]),
            float(str(data).split("=")[3].split(",")[0]), str(data).split("=")[4].split(",")[0] == 'True')

    if time.time() - _last_time > 4:
        _last_time = time.time()
        
        # a. distance angulaire & metriques entre les avions 
        if mav1_Etape == "SYNCHRONISATION":    # des avions en cercles
            # a.i azimuth des avions
            _mav1_bearing = gps_bearing(_location_attente_mav1.lat, _location_attente_mav1.lon, v.location.lat, v.location.lon)
            _mav0_bearing = gps_bearing(_location_attente_mav0.lat, _location_attente_mav0.lon, _mav0_location.lat, _mav0_location.lon)
            _distance_angulaire = (_mav1_bearing - _mav0_bearing) % 360
            # a.ii distance entre les avions
            if _distance_angulaire > 180: _distance_angulaire -= 360  #angles ds -180 +180; negatif qd esclave en retard
            _distance_curviligne = _distance_angulaire / 360 * 2 * 3.14159 * _WP_LOITER_RAD
            # a.iii si l'esclave est a la tengete, alors passage a l'etape RATTRAPAGE
            _distance_angulaire_tangente = ( (_direction_piste-90) - _mav1_bearing ) % 360
            if _distance_angulaire_tangente > 180: _distance_angulaire_tangente -= 360  #negatif avant tangente
            if abs(_distance_curviligne) < 10 and abs(_distance_angulaire_tangente) < 15:
                print "Esclave synchronise avec le maitre --> mode RATTRAPAGE"
                v.mode = VehicleMode("AUTO")
                mav1_Etape = "RATTRAPAGE"
                # dire a avion maitre de faire un tour puis de passer en mode auto
                _mav1_client_socket.sendto( "top_synchro", _mav0_server_addr)
                log_file = open('log_mav1sync.txt','a')
                log_file.write("esclave synchronise sur maitre --> mode RATTRAPAGE")
                log_file.close()

        # b. esclave commence mais le maitre fait encore un tour 
        elif mav1_Etape == "RATTRAPAGE":     
            # chemin que mav 1 a fait depuis la tengente
            _chemin_mav1 = gps_distance( _location_tengente_mav1.lat, _location_tengente_mav1.lon, v.location.lat, v.location.lon )
            # chemin que mav 0 doit fait pour finir son tour
            _mav0_bearing = gps_bearing(_location_attente_mav0.lat, _location_attente_mav0.lon, _mav0_location.lat, _mav0_location.lon)
            _angle_depuis_tangente = ( _mav0_bearing - (_direction_piste-90) ) % 360
            _chemin_mav0 = _angle_depuis_tangente / 360 * 2 * 3.14159 * _WP_LOITER_RAD
            _distance_curviligne = _chemin_mav1 - _chemin_mav0
            if _chemin_mav1 > 2*3.14159*_WP_LOITER_RAD :
                print "Esclave a hauteur du maitre --> mode PASSAGE"
                mav1_Etape = "PASSAGE"
                log_file = open('log_mav1sync.txt','a')
                log_file.write("avion a hauteur du maitre --> mode PASSAGE")
                log_file.close()

        # c. esclave commence mais le maitre fait encore un tour 
        elif mav1_Etape == "PASSAGE" : 
            _chemin_mav0 = gps_distance( _location_depart_mav0.lat, _location_depart_mav0.lon, _mav0_location.lat, _mav0_location.lon)
            _chemin_mav1 = gps_distance( _location_depart_mav1.lat, _location_depart_mav1.lon, v.location.lat, v.location.lon )
            _distance_curviligne = _chemin_mav1 - _chemin_mav0
            if _chemin_mav1 > _longueur_passage :
                mav1_Etape = "FIN"
                v.mode = VehicleMode("GUIDED")
                v.commands.goto(_location_attente_mav1)
                v.flush()
                v.parameters['TRIM_ARSPD_CM']=2000  #2200 par defaut pour le rascal
                v.flush()
                print "passage en mode fin --> mode guided"
                print "TRIM_ARSPD_CM = "+str(v.parameters['TRIM_ARSPD_CM'])

        elif mav1_Etape == "FIN" :    
            pass

        # regulateur de vitesse
        _delta_vitesse =  -_distance_curviligne / 5
        if _delta_vitesse >  10: _delta_vitesse = 10
        if _delta_vitesse < -10: _delta_vitesse = -10
        cmd_TRIM_ARSPD_CM = 2000+100*_delta_vitesse
        v.parameters['TRIM_ARSPD_CM']= int(cmd_TRIM_ARSPD_CM)                # 2200 pour rascal
        v.flush()

        # logs du regulateur : latences a verifier, integrateur a ajouter, derive inutile a cause de la vitesse max
        log_file = open('log_mav1sync.txt','a')
        log_file.write("\n" + str(_last_time) + "\t" + str(_distance_curviligne) + "\t"+str(_delta_vitesse) + "\t"+str(cmd_TRIM_ARSPD_CM) + "\t"+str(v.parameters['TRIM_ARSPD_CM']))
        log_file.close()


print "Server Stopped"
_mav1_server_socket.close()
_mav1_client_socket.close()
