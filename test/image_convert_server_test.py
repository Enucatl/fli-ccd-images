import socket
import os

if __name__ == '__main__':
    HOST, PORT = "localhost", 8889
    try:
        os.remove("test.root")
    except OSError:
        pass
    #subprocess.call(
            #"python python/image_convert_server.py test {0} &".format(PORT),
            #shell=True)
    with open("test/image_file_name") as data:
        # Create a socket (SOCK_STREAM means a TCP socket)
        for line in data:
            # Connect to server and send data
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((HOST, PORT))
                print("connected")
                sock.sendall(line)
                print "Sent: {}".format(line)

                # Receive data from the server and shut down
                received = sock.recv(1024)
                print "Received: {}".format(received)
            except (socket.error, KeyboardInterrupt) as error:
                print(error)
                break
            finally:
                sock.close()


    line = "close_server"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(line)
    received = sock.recv(1024)
    print "Received: {}".format(received)
