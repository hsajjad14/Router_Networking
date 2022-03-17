# Import socket module
import socket
import argparse 
 
def Main(input_port, input_ip_dest, ttl, input_file):
    # local host IP '127.0.0.1'
    host = input_ip_dest
 
    # Define the port on which you want to connect
    port = int(input_port)
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect((host,port))

    f = open(input_file, "r")


    # message you send to server
    message = f.read()
    s.send(message.encode('ascii'))
    #while True:
 
        # message sent to server
     #   s.send(message.encode('ascii'))
 
        # message received from server
        #data = s.recv(1024)
 
        # print the received message
        # here it would be a reverse of sent message
        #print('Received from the server :',str(data.decode('ascii')))
 
        # ask the client whether he wants to continue
        #ans = input('\nDo you want to continue(y/n) :')
        #if ans == 'y':
        #    continue
        #else:
        #    break
    # close the connection
    s.close()
 
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='take in port number, destination ip and ttl')
    argparser.add_argument('port', help="port number")
    argparser.add_argument('ip_dest', help="destination ip address")
    argparser.add_argument('ttl', help="time to live")
    argparser.add_argument('file', help="path of file to send")
    args = argparser.parse_args()

    Main(args.port, args.ip_dest, args.ttl, args.file)


