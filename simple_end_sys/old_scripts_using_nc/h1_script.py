import argparse
import subprocess
import os


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='take in port number, destination ip and ttl')
    argparser.add_argument('port', help="port number")
    argparser.add_argument('ip_dest', help="destination ip address")
    argparser.add_argument('ttl', help="time to live")
    argparser.add_argument('file', help="path of file to send")
    args = argparser.parse_args()

    # initialize
    command = "nc "+ "255.255.255.255" + " " + str(args.port) + " < " + str(args.file)
    os.system(command)

    # send function
    command = "nc "+ str(args.ip_dest) + " " + str(args.port) + " -M " + str(args.ttl) + " < " + str(args.file)
    os.system(command)
