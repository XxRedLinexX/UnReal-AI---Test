
import numpy as np
from grabscreen import grab_screen
import cv2
import time
from models import sentnet_color_2d
from User_Input import key_check
from send_clicks import fire
import random
import ctypes

WIDTH = 160
HEIGHT = 280
LR = 1e-3
frame_count = 3
EPOCHS = 10
MODEL_NAME = 'sentnet_color_2d-try1'

user32 =  ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
roip1 = int((screensize[0] / 2) - 160)
roip2 = int((screensize[1] / 2) - 280)
roip3 = int((screensize[0] / 2) + 160)
roip4 = int((screensize[1] / 2) + 280)

SendInput = ctypes.windll.user32.SendInput

l_press = [1,0,0,0,0]
l_release = [0,1,0,0,0]
r_press = [0,0,1,0,0]
r_release = [0,0,0,1,0]
nk = [0,0,0,0,1]
    

model = sentnet_color_2d(WIDTH, HEIGHT, frame_count, LR, output = 5)
model.load(MODEL_NAME)

def main():
    #last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last = 0

    paused = False
    while(True):
        
        if not paused:
            # 800x600 windowed mode
            screen = grab_screen(region=(roip1,roip2,roip3,roip4))
            #print('loop took {} seconds'.format(time.time()-last_time))
            #last_time = time.time()
            screen = cv2.resize(screen, (160,280))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            prediction = model.predict([screen.reshape(160,280,3)])[0] #(160,280,1)])[0]
            print(prediction)
            
            if np.argmax(prediction) == np.argmax(l_press):
                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0,0)
                #ctypes.windll.user32.mouse_event(4, 0, 0, 0,0)
                last = 1
            if np.argmax(prediction) == np.argmax(l_release):
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0,0)
                last = 2
            if np.argmax(prediction) == np.argmax(r_press):
                ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0,0)
                #ctypes.windll.user32.mouse_event(10, 0, 0, 0,0)
                last = 3
            if np.argmax(prediction) ==np.argmax( r_release):
                ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0,0)
                last = 4
            if np.argmax(prediction) == np.argmax(nk):
                if last == 1:
                    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0,0)
                    last = 5
                elif last == 3: 
                    ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0,0)
                else:
                    last = 5
                    pass
            #fire(np.argmax(prediction))
            
        keys = key_check()

        # p pauses game and can get annoying.
        if 'L' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                time.sleep(1)

main() 