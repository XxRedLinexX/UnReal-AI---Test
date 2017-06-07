import numpy as np
from grabscreen import grab_screen
import ctypes
import cv2
import time
from User_Input import mouse_click
from keyboard import listen
import os
from ctypes import windll, Structure, c_ulong, byref
import win32api

user32 =  ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

starting_value = 1

class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

while True:
    file_name = 'training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        
        break


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0,0,0,0,0,0,0,0,0]

    if 'w' in keys and 'a' in keys:
        output = wa
    elif 'w' in keys and 'd' in keys:
        output = wd
    elif 's' in keys and 'a' in keys:
        output = sa
    elif 's' in keys and 'd' in keys:
        output = sd
    elif 'w' in keys:
        output = w
    elif 's' in keys:
        output = s
    elif 'a' in keys:
        output = a
    elif 'd  ' in keys:
        output = d
    else:
        output = nk
    return output


def MousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x,pt.y]


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
            screen = grab_screen(region=(0,0,screensize[0],screensize[1]))
            last_time = time.time()
            # resize to something a bit more acceptable for a CNN
            #screen = cv2.resize(screen, (480,270))  Original
            screen = cv2.resize(screen, (360,202))
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            
            keys = listen()
            clicks = mouse_click()
            output = keys_to_output(keys)
            pos = MousePosition()
            training_data.append([screen,output,pos,clicks])

            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
##            cv2.imshow('window',cv2.resize(screen,(640,360)))
##            if cv2.waitKey(25) & 0xFF == ord('q'):
##                cv2.destroyAllWindows()
##                break

            if len(training_data) % 100 == 0:
                print(len(training_data))
                
                if len(training_data) == 500:
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = 'training_data-{}.npy'.format(starting_value)

                    
        keys = listen()
        if 'k' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main(file_name, starting_value)
