#!/bin/bash

case $1 in 
    -s|--sitl)
        case  $2 in
            mav0)
                mavproxy.py --master=127.0.0.1:14550 --out=udp:127.0.0.1:14551 --console --load-module=droneapi.module.api --aircraft=avionSITL
                ;;
            mav1)
                mavproxy.py --master=127.0.0.1:14560 --out=udp:127.0.0.1:14561 --console --load-module=droneapi.module.api --aircraft=avionSITL
                ;;
            *)
                echo "mav0 ou mav1"
        esac
        ;;
    -a|--apm)
        mavproxy.py \
            --master=/dev/cu.usbmodem411 \
            --baudrate=115200 \
            --aircraft=TestPlane \
            --console \
            --load-module=droneapi.module.api \
            --out=udp:127.0.0.1:14550 
        ;;
    -c|--cli)
        mavproxy.py --master=/dev/tty.usbmodem411 --setup --baudrate=115200
        ;;
    -d|--debug)
        echo "DEBUG: Nombre d'arguments : "$#
        echo "DEBUG: Le premier : "$1
        echo "DEBUG: Le deuxieme : "$2
        echo "DEBUG: Le troisieme : "$3
        ;;
    -h|--help|*)
        {
        cat << EOF
parser v0.1 de juju

usage : parser.sh [options]

 -s , --sitl     : [-s mav0 || -s mav1] pour la simulation SITL
 -a , --apm      : conection apm 2.5
 -c , --cli      : connection series (CLI pour l'APM)
 -d , --debug    : echo les arguements de la ligne de commande 
 -h , --help     : montre cette aide
EOF
}
esac
