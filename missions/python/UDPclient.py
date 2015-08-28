#liste des sockets dans /etc/services
import socket

def Main():
    host = '127.0.0.1'
    port = 14548

    server = ('127.0.0.1',14549)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    message = raw_input("-> ")
    while message != 'q':
        s.sendto(message, server)
#        data, addr = s.recvfrom(1024)
#        print 'Received from server: ' + str(data)
        message = raw_input("-> ")
    s.close()

if __name__ == '__main__':
    Main()
