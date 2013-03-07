#!/usr/bin/env python
from __future__ import division, print_function

import SocketServer
import pexpect
from datetime import datetime

#global control variable to check that the scan is ongoing
scanning = False

command = "./bin/convert_scan_online {0}".format(folder)
converter = pexpect.spawn(command)

class ImageConvertTCPServer(SocketServer.TCPServer):
    """eliminate 'address already in use' error
    http://stackoverflow.com/questions/10613977/a-simple-python-server-using-simplehttpserver-and-socketserver-how-do-i-close-t?lq=1"""
    allow_reuse_address = True
    request_queue_size = 10000

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        return_code = 0
        if self.data == "close_server":
            global scanning
            scanning = False
            return_code = 1
        else:
            global converter
            converter.expect("next image file name:")
            converter.sendline(self.data)
        print(datetime.now(), return_code)
        send_string = str(return_code)
        print("return code", return_code)
        self.request.sendall(send_string + "\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='''open server for SPEC
            that will convert raw images to ROOT format''')
    parser.add_argument('port', metavar='PORT',
            nargs='?', default=8961, help='port for the server on localhost')
    parser.add_argument('folder', metavar='FOLDER',
            nargs=1, help='folder where the RAW files will be saved')
    args = parser.parse_args()
    port = args.port
    folder = args.folder[0]

    host = ""
    server = ImageConvertTCPServer((host, port), MyTCPHandler)
    scanning = True

    #scanning changed to False when client sends "close_server" command
    while scanning:
        print("ready for request")
        server.handle_request()

    converter.sendline("bye")
    print("bye")
