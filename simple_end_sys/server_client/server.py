# import socket programming library
import socket
import argparse
import netifaces as ni

# import thread module
from _thread import *
import threading
from mininet.topo import Topo
 
print_lock = threading.Lock()
 
# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        # reverse the given string from client
        #data = data[::-1]

        # send back reversed string to client
        #c.send(data)

        # print data from the client
        print(data)

    # connection closed
    c.close()


def sendMsg(input_port, input_ip_dest, ttl, input_file):
    host = input_ip_dest

    # Define the port on which you want to connect
    port = int(input_port)

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, int(ttl))

    # connect to server on local computer
    try:
        s.connect((host,port))
    except socket.error as msg:
        print("could not send message to " + str(host))
        return 0

    f = open(input_file, "r")

    # message you send to server
    message = f.read()
    s.send(message.encode('ascii'))

    s.close()

    return 1


def broadcast(input_port):
    host = "255.255.255.255"
    port = int(input_port)
    msg = b'broadcasting existence of host\n'

    # get the IP address(es) that this host uses to broadcast
    # source: https://www.semicolonworld.com/question/53556/how-can-i-get-the-ip-address-of-eth0-in-python
    interfaces = ni.interfaces()
    ipsToBroadcast = []
    for i in interfaces:
        if i != 'lo':
            ipsToBroadcast.append(ni.ifaddresses(i)[ni.AF_INET][-1]['broadcast'])

    for ip in ipsToBroadcast:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 0)
        s.bind((ip,port))
        s.sendto(msg, (host, port))
        s.close()

    '''
    # connect to server on local computer
    try:
        s.connect((host,port))
    except socket.error as msg:
        print("could not broadcast")
        return 0

    # message you send to server
    message = "broadcasting existence of host"
    s.send(message.encode('ascii'))

    s.close()
    '''


def Main(input_port, initialize, snd_msg_1st, input_ip_dest, ttl, input_file):
    if initialize.lower() == "true":
        broadcast(input_port)

    if snd_msg_1st.lower() == "true":
        sendMsg(input_port, input_ip_dest, ttl, input_file)

    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = int(input_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    f = open(input_file, "r")

    # message you send to ip
    message = f.read()
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()
 
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
 
 
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='take in port number, a boolean flag for initialize, a boolean flag for whether the server should send a message before listening, destination ip, ttl, and a path to the file to send')
    argparser.add_argument('port', help="port number")
    argparser.add_argument('initialize', help="boolean flag; true iff you want to initialize this server and broadcast its existence")
    argparser.add_argument('snd_msg_1st', help="boolean flag; true iff you want server to send a message before listening")
    argparser.add_argument('ip_dest', help="destination ip address")
    argparser.add_argument('ttl', help="time to live")
    argparser.add_argument('file', help="path of file to send")
    args = argparser.parse_args()

    Main(args.port, args.initialize, args.snd_msg_1st, args.ip_dest, args.ttl, args.file)

