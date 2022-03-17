import argparse
import subprocess
import os


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='take in port number, destination ip and ttl')
    argparser.add_argument('port', help="port number")

    # argparser.add_argument('ip_dest', help="destination ip address")
    # argparser.add_argument('ttl', help="time to live")

    args = argparser.parse_args()

    # print(args.port, args.ip_dest, args.ttl)

    command = 'nc -l ' + str(args.port)
    os.system(command)
    # process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()
    # print("output = ", output)
