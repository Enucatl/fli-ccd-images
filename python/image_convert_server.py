#!/usr/bin/env python
from __future__ import division, print_function

import SocketServer
import subprocess

command = "./bin/add_image_to_root_file"
#programme = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        #stdin=subprocess.PIPE)

class ShutdownServer(Exception):
    pass

class ImageConvertServer(SocketServer.TCPServer):

    def handle_error(self, *args, **kwargs):

        if self.data == "close_server":
            print("shutting down server...")
            self.shutdown()
        super(ImageConvertServer, self).handle_error(*args, **kwargs)


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
        if self.data == "close_server":
            raise ShutdownServer("got close_server command!")
        # just send back the same data, but upper-cased
        #programme.communicate(self.data)
        programme = "{0} {1}".format(
            command,
            self.data)
        print(programme)
        return_code = subprocess.call(programme,
            shell=True)
        print("return code", return_code)
        self.request.sendall(self.data)

if __name__ == "__main__":
    HOST, PORT = "", 8888

    server = ImageConvertServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
