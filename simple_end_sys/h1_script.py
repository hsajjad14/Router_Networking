import argparse


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='take in port number, destination ip and ttl')
    argparser.add_argument('PORT', help="port number")

    argparser.add_argument('IP_DEST', help="destination ip address")
    argparser.add_argument('TTL', help="time to live")

    args = argparser.parse_args()

