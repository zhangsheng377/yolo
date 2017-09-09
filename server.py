import socket

'''server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5005))
server_socket.listen(5)
import os



while (1):
    client_socket, address = server_socket.accept()
    print("Conencted to - ", address, "\n")
    fp = open("tmp.jpg", 'wb')
    while True:
        str = client_socket.recv(512)
        if not str:
            break
        fp.write(str)
    fp.close()
    print("Data Received successfully")
'''
import sys, os

sys.path.append(os.path.join(os.getcwd(), 'python/'))
import darknet as dn

net = dn.load_net("cfg/yolo.cfg".encode(), "yolo.weights".encode(), 0)
meta = dn.load_meta("cfg/coco.data".encode())

r = dn.detect(net, meta, "data/dog.jpg".encode())
print(r)
