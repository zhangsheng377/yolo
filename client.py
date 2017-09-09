import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.31.240", 5007))

img = open("dog.jpg", 'rb')
string = "".encode()
while True:
    strng = img.readline()
    if not strng:
        break
    string += strng
img.close()
if string:
    client_socket.send(string)
    print("Data sent successfully")
    string = client_socket.recv(1024)
    print(string)
client_socket.close()
exit()
