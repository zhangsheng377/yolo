import socket
import darknet as dn

net = dn.load_net("cfg/yolo.cfg".encode(), "yolo.weights".encode(), 0)
meta = dn.load_meta("cfg/coco.data".encode())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5007))
server_socket.listen(5)

while True:
    client_socket, address = server_socket.accept()
    print("Conencted to - ", address)
    fp = open("tmp.jpg", 'wb')
    while True:
        string = client_socket.recv(512)
        if not string:
            break
        if string == "ISOVER,REQUESTJSON":
            break
        fp.write(string)
    fp.close()
    print("Data Received successfully")
    r = dn.detect(net, meta, "tmp.jpg".encode())
    print(r)
    client_socket.send("".join(r))
    client_socket.close()
