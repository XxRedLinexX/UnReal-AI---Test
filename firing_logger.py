import numpy as np
from grabscreen import grab_screen
import ctypes
import cv2
import time
from User_Input import key_check, mouse_click
import os
import win32api

user32 =  ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

starting_value = 1

roip1 = int((screensize[0] / 2) - 160)
roip2 = int((screensize[1] / 2) - 280)
roip3 = int((screensize[0] / 2) + 160)
roip4 = int((screensize[1] / 2) + 280)

while True:
    file_name = 'firing_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        
        break


def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while(True):
        
        if not paused:
            screen = grab_screen(region=(roip1,roip2,roip3,roip4))
            last_time = time.time()
            # resize to something a bit more acceptable for a CNN
            #screen = cv2.resize(screen, (480,270))  Original
            screen = cv2.resize(screen, (160,280))
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            
            clicks = mouse_click()

            training_data.append([screen,clicks])

            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

            if len(training_data) % 100 == 0:
                print(len(training_data))
                
                if len(training_data) == 500:
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = 'firing_data-{}.npy'.format(starting_value)

                    
        keys = key_check()
        if 'J' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main(file_name, starting_value)