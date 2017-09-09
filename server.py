import socket
import darknet as dn

net = dn.load_net("cfg/yolo.cfg".encode(), "yolo.weights".encode(), 0)
meta = dn.load_meta("cfg/coco.data".encode())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5007))
server_socket.listen(5)
file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file_socket.bind(("", 5008))
file_socket.listen(5)

while True:
    client_socket, address = server_socket.accept()
    print("Conencted to - ", address)
    file_client_socket, address = server_socket.accept()
    print("File Conencted to - ", address)
    isEmpty = True
    fp = open("tmp.jpg", 'wb')
    while True:
        string = file_client_socket.recv(512)
        if not string:
            break
        fp.write(string)
        isEmpty = False
    fp.close()
    file_client_socket.close()
    if not isEmpty:
        print("Data Received successfully")
        r = dn.detect(net, meta, "tmp.jpg".encode())
        print(r)
        client_socket.send("".join(r))
    client_socket.close()
