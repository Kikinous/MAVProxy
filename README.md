MAVProxy

This is a MAVLink ground station written in python. 

Please see http://Dronecode.github.io/MAVProxy/ for more information

This ground station was developed as part of the CanberraUAV OBC team
entry

Fork by Kikinous
----------------
**The [installation branch](https://github.com/Kikinous/MAVProxy/tree/installation) is up to date on Sept 2015**

My goal is to get a few planes flying in formation.
It is assumed to fly in CAAP64 nearby Pau, France.

For now, I am using mavproxy runnning on the GCS.
For now, it is only working with a SITL simulation.
For now, it is working with droneapi code located in the mission folder:
- mav0wait.py : leader plane waits
- mav1wait.py : follower plane waits
- mav0sync.py : leader plane sends its location while it is performing a mission
- mav1sync.py : follower plane gets levelled with the leader plane
- Aide_memoire.md : some notes
![alt tag](https://raw.githubusercontent.com/Kikinous/MAVProxy/installation/missions/formation.png)


License
-------

MAVProxy is released under the GNU General Public License v3 or later

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Dronecode/MAVProxy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
