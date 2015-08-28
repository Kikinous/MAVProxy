SIMULATION
==========

osx$ vagrant ssh
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ screen -d -R
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ screen -d -R -t ecran0
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ sim_vehicle.sh -v ArduPlane


Notes :
- Toujours lancer sim_vehicules.sh depuis ArduPlane/ pour convercer les parametres sauvegardes 
    dans ArduPlane/eeprom.bin
- Commandes screen :
    ctrl-a S      : split horizontally
    ctrl-a ctrl-a : flip flop windows
    ctrl-a 1      : window 1
    ctrl-a tab    : jump to next region
    ctrl-a X      : remove current region
    ctrl-a [      : enter copy mode (to scroll upward)
    ctrl-a c      : create

Simulation d'une deuxieme instance
----------------------------------
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ sim_vehicle.sh -I 1 -v ArduPlane




Mavproxy dans OS-X
------------------
osx$ mavproxy.py --master=127.0.0.1:14550 --out=udp:127.0.0.1:14551
MAV> param load /Users/julienborghetti/Documents/Code/github/ardupilot/Tools/autotest/ArduPlane.parm
MAV> wp load /Users/julienborghetti/Documents/Code/github/ardupilot/Tools/autotest/ArduPlane-Missions/CMAC-toff-loop.txt
MAV> wp load /Users/julienborghetti/Documents/Code/github/sitl_session/missionCAAP54.txt
MAV> wp list
MAV> wp loop
MAV> wp list

MAV> arm throttle
MAV> mode auto


Notes :
- MAV> param set TRIM_ARSPD_CM 2200     //
  MAV> guided 43.102 -0.162 100         //Saint pe de bigorre
  MAV> guided 43.232 -0.162 100         //CAAP64
  MAV> mode guided                      //
  MAV> link list                        //
  MAV> output                           //


APM Planner dans OS-X
---------------------
Creer un lien sur 127.0.0.1:14551


VRAC : COMMANDES UTILISEES
==========================
## Commandes dans mavproxy :
output : pour voir si mavproxy redirige bien les packets

## Nouvelle mission
1. Ajout de *CAAP64* dans locations.txt
   * format de locations.txt 
       `vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ ./ArduPlane.elf  --help`
       >Options:
       >    --home HOME        set home location (lat,lng,alt,yaw)
       >    --model MODEL      set simulation model
       >    --wipe             wipe eeprom and dataflash
       >    --rate RATE        set SITL framerate
       >    --console          use console instead of TCP ports
       >    --instance N       set instance of SITL (adds 10*instance to all port numbers)
       >    --speedup SPEEDUP  set simulation speedup
       >    --gimbal           enable simulated MAVLink gimbal
       >    --autotest-dir DIR set directory for additional files

   * Altitude du terrain ?
       `osx$ Python mp_elevation.py --lat=43.23356 --lon=-0.104083`
       >Altitude at (43.233560, -0.104083) is 415 m. Pulled at 7.4 FPS

   * Ajout de la ligne CAAP64=43.23356,-0.104083,415,170
       vi /Users/julienborghetti/Documents/Code/github/ardupilot/Tools/autotest/locations.txt

2. Demmarrage de sim
   `vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ sim_vehicle.sh -v ArduPlane -L CAAP64``

   
