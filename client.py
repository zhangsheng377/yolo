import socket
import json
from PIL import Image
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os

print("Initing......")

GPIO.setmode(GPIO.BOARD)

botton = 32
# GPIO.setup(botton, GPIO.IN)
GPIO.setup(botton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# time.sleep(2)

# while (True):
#    botton_input = GPIO.input(botton)
#    print(type(botton_input), botton_input)
#    time.sleep(0.5)

camera = PiCamera()
camera.start_preview()
time.sleep(5)

print("Init over.\nworking......")

while (True):
    botton_input = GPIO.input(botton)
    # print(type(botton_input), botton_input)
    if (botton_input == 1):
        time.sleep(0.3)
        botton_input = GPIO.input(botton)
        # print(type(botton_input), botton_input)
        if (botton_input == 1):
            # if(GPIO.wait_for_edge(botton, GPIO.RISING, timeout=5000)):

            print("start capturing......")

            camera.capture('camera.jpg')

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("192.168.43.78", 5007))
            file_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            file_client_socket.connect(("192.168.43.78", 5008))

            file_name = "camera.jpg"

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
            objs_str = ""
            for element in j:
                print("在您的", end="")
                objs_str += "在您的"
                if element[2][0] + element[2][2] < im.size[0] / 3:
                    print("左侧", end="")
                    objs_str += "左侧"
                elif element[2][0] > im.size[0] / 3 * 2:
                    print("右侧", end="")
                    objs_str += "右侧"
                else:
                    print("前方", end="")
                    objs_str += "前方"
                if element[2][1] + element[2][3] > im.size[1] / 3 * 2:
                    print("近处", end="")
                    objs_str += "近处"
                elif element[2][1] + element[2][3] > im.size[1] / 3:
                    print("稍远处", end="")
                    objs_str += "稍远处"
                else:
                    print("远处", end="")
                    objs_str += "远处"
                print("有一个", element[0])
                # objs_str += "有一个"
                objs_str += "有"
                objs_str += element[0]
                objs_str += "\n"
            # print(objs_str)

            command = "ekho \"" + objs_str + "\" -o output.wav"
            os.system(command)
            os.system("sudo aplay output.wav")

    time.sleep(0.5)

exit()
