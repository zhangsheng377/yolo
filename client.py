import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.31.240", 5007))

img = open("dog.jpg", 'rb')
while True:
    string = img.read(512)
    if not string:
        break
    client_socket.send(string)
img.close()
client_socket.close()
print("Data sent successfully")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5008))
server_socket.listen(5)
client_socket, address = server_socket.accept()
print("Conencted to - ", address)
string = client_socket.recv(1024)
print(string)
client_socket.close()
server_socket.close()
exit()
