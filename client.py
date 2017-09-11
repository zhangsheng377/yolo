import socket
import json
from PIL import Image

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.31.240", 5007))
file_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file_client_socket.connect(("192.168.31.240", 5008))

file_name = "dog.jpg"

im = Image.open(file_name)
print('格式', im.format, '，分辨率', im.size, '，色彩', im.mode)
max_size = 500
if max(im.size[0], im.size[1]) > max_size:
    if im.size[0] > im.size[1]:
        im.thumbnail((max_size, max_size / im.size[0] * im.size[1]))
    else:
        im.thumbnail((max_size / im.size[1] * im.size[0], max_size))
im.save('tmp.jpg', 'JPEG', quality=90)
file_name = "tmp.jpg"
print('格式', im.format, '，分辨率', im.size, '，色彩', im.mode)

img = open(file_name, 'rb')
while True:
    string = img.read(512)
    if not string:
        break
    file_client_socket.send(string)
img.close()
file_client_socket.close()
print("Data sent successfully")
s = client_socket.recv(1024)
client_socket.close()
ss = str(s, encoding="utf-8")
j = json.loads(ss)
print(j)
for element in j:
    print("在您的", end="")
    if element[2][0] + element[2][2] < im.size[0] / 3:
        print("左侧", end="")
    elif element[2][0] > im.size[0] / 3 * 2:
        print("右侧", end="")
    else:
        print("前方", end="")
    if element[2][1] + element[2][3] > im.size[1] / 3 * 2:
        print("近处", end="")
    elif element[2][1] + element[2][3] > im.size[1] / 3:
        print("稍远处", end="")
    else:
        print("远处", end="")
    print("有一个", element[0])

exit()
