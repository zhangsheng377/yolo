import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.31.240", 5005))

img = open("dog.jpg", 'rb')
while True:
    string = img.read(512)
    if not string:
        break
    client_socket.send(string)
img.close()
print("Data sent successfully")
client_socket.close()
exit()
