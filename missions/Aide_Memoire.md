SIMULATION
==========

osx:ardupilot/$ vagrant up
osx:ardupilot/$ vagrant ssh     ~~ run /Tools/vagrant/shellinit.sh ~~
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ screen -t simul0 
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ sim_vehicle.sh -L CAAP64 -v ArduPlane

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

Simulation d'un deuxieme avion
------------------------------
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ screen -t simul1 
vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ sim_vehicle.sh -I 1 -L CAAP64 -v ArduPlane

Mavproxy dans OS-X
------------------
osx:Code/MAVProxy/missions/$ ./start_mavproxy.sh -s mav0
MAV> param load ArduPlane.parm  // sauves dans eeprom.bin quand stil fini
MAV> param set SYSID_THISMAV 1
MAV> wp load tkoff
MAV> arm throttle
MAV> mode auto

Notes :
- MAV> param set TRIM_ARSPD_CM 2200     //
  MAV> guided 43.102 -0.162 100         //Saint pe de bigorre
  MAV> mode guided                      //
  MAV> link list                        //
  MAV> output                           //
  MAV> param set SYSID_THISMAV 1        //
  MAV> param show SYSID_THISMAV         //
- pour atterrir
  MAV> 

VRAC : COMMANDES UTILISEES
==========================

## Nouvelle mission
1. Ajout de *CAAP64* dans locations.txt
   * format de Tools/autotest/locations.txt  (dans github/ardupilot/ ou /vagrant/ : ce sont les memes)
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
   `vagrant@vagrant-ubuntu-trusty-32:/vagrant/ArduPlane$ sim_vehicle.sh -v ArduPlane -L CAAP64`

3. Sequence d'atterrissage depuis l'ouest 
fichier : land_W2E.txt
3	0	3	16	0	0	0	0	43.2335413452921458	-0.111880302429199219	50	1
4	0	3	16	0	0	0	0	43.2319232702038576	-0.111150741577148438	50	1
5	0	3	21	0	0	0	0	43.233304890139479	-0.105078220367431641	0	0
Pour le rascal :
- LAND_FLARE_ALT    = 3
- LAND_FLARE_SEC    = 0       ~~ 5 par default ~~
- LAND_PITCH_CD     = 100
- TECS_LAND_ARSPD   = 10      ~~ -1 par default ~~
- TECS_LAND_SPDWGT  = 1

- RNGFND_LANDING    = 0
- RTL_AUTOLAND      = 0 

   
