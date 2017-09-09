import socket
import darknet as dn

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5006))
server_socket.listen(5)

net = dn.load_net("cfg/yolo.cfg".encode(), "yolo.weights".encode(), 0)
meta = dn.load_meta("cfg/coco.data".encode())

while True:
    client_socket, address = server_socket.accept()
    print("Conencted to - ", address)
    fp = open("tmp.jpg", 'wb')
    while True:
        string = client_socket.recv(512)
        if not string:
            break
        fp.write(string)
    fp.close()
    print("Data Received successfully")
    r = dn.detect(net, meta, "tmp.jpg".encode())
    print(r)
    client_socket.send("".join(r))
    client_socket.close()
