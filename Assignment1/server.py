r'''
Date: 2022-01-27 15:29:49
LastEditors: Kunyang Xie
LastEditTime: 2022-01-28 01:01:51
FilePath: \Assignment1\server.py
'''
import sys
import re
import random
from socket import *


class Server:
    def __init__(self, req_code):
        self.req_code = req_code

    def negotiate(self):
        serverPort = 8080
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', serverPort))
        print('The server is ready to receive')
        while True:
            message, clientAddress = serverSocket.recvfrom(2048)
            mode = message.decode()[:4]
            dash = re.search(r'/', message.decode())

            get_req_code = message.decode()[dash.span()[1]:]
            if get_req_code == self.req_code:
                if mode == 'PORT':
                    r_port = int(message.decode()[4:dash.span()[0]])
                elif mode == 'PASV':
                    r_port = random.randint(8000, 8888)
                else:
                    print('Error: Undefined mode')
                    continue
                acknowledgement = '1' + str(r_port)
                serverSocket.sendto(acknowledgement.encode(), clientAddress)
                serverSocket.close()
            else:
                acknowledgement = '0'
                serverSocket.sendto(acknowledgement.encode(), clientAddress)
                print('req_code wrong')
                continue

    def transaction(self):
        ...


def main():
    # Obtain command
    argv = sys.argv
    req_code = argv[1]
    file_to_send = argv[2]

    server = Server(req_code=req_code)
    server.negotiate()


if __name__ == '__main__':
    main()

# python server.py 11 bbb
