import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.31.240", 5007))
file_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file_client_socket.connect(("192.168.31.240", 5008))

img = open("dog.jpg", 'rb')
while True:
    string = img.read(512)
    if not string:
        break
    file_client_socket.send(string)
img.close()
file_client_socket.close()
print("Data sent successfully")
string = client_socket.recv(1024)
print(string)
client_socket.close()
exit()
