import numpy as np
import pandas as pd
import cv2
import time
from random import shuffle
import os


starting_value = 1
train_data = np.load('firing_data-{}.npy'.format(starting_value))

def balance(starting_value, train_data):
    starting_value = starting_value
    train_data = train_data

    df = pd.DataFrame(train_data)

    r_press = [1,0,0,0,0]
    r_release = [0,1,0,0,0]
    l_press = [0,0,1,0,0]
    l_release = [0,0,0,1,0]
    nk = [0,0,0,0,1]


    r_start = [] # r actually l
    r_end = []
    r_concat = []
    l_start = [] # l actually r  - corrected later
    l_end = []
    l_concat = []
    all_press = []


    for i,f in enumerate(df[1]):
        if f == [1]:
            r_start.append(i)
        if f == [10]:
            r_end.append(i)
        if f == [2]:
            l_start.append(i)
        if f == [20]:
            l_end.append(i)
        if len(f) >= 2:
            for i in f:
                if i == 1:
                    r_start.append(i)
                if i == 10:
                    r_end.append(i)
                if i == 2:
                    l_start.append(i)
                if i == 20:
                    l_end.append(i)


    if len(l_start) < len(l_end):
        del l_end[0]

    if len(r_start) < len(r_end):
        del r_end[0]

    if len(r_start) > len(r_end):
        r_end.append(len(df[1]))

    if len(l_start) > len(l_end):
        l_end.append(len(df[1]))
    '''
    print(r_start)
    print(r_end)
    print(len(l_start))
    print(len(l_end))
    '''

 
    counter = 0
    add = 0
    for i,f in enumerate(r_start):
        add = (r_end[i] - r_start[i])
        counter = r_start[i]
        r_concat.append(f)
        for x in range(add):
            counter += 1
            if counter <= (r_end[i]-1):        
                r_concat.append(counter)


    counterl = 0
    addl = 0
    for i,f in enumerate(l_start):
        addl = (l_end[i] - l_start[i])
        counterl = l_start[i]
        l_concat.append(f)
        for x in range(addl):
            counterl += 1
            if counterl <= (l_end[i]-1):        
                l_concat.append(counterl)

    for i,f in enumerate(df[1]):
        if i in r_concat:
            all_press.append(i)
        if i in l_concat:
            all_press.append(i)
        if i in l_end:
            all_press.append(i)
        if i in r_end:
            all_press.append(i)
        
    
    for i,f in enumerate(df[1]):
        if i in r_concat:
            df[1].set_value(i,r_press)
        if i in l_concat:
            df[1].set_value(i,l_press)
        if f == [10]:
            df[1].set_value(i,r_release)
        if f == [20]:
            df[1].set_value(i,l_release)
        if i not in all_press:
            df[1].set_value(i,nk)
        


    left = []
    right = []
    no_key = []

    for i,f in enumerate(df[1]):
        if f == r_press:
            left.append([i,f])
        elif f == r_release:
            left.append([i,f])
        elif f == l_press:
            right.append([i,f])
        elif f == l_release:
            right.append([i,f])
        elif f == nk:
            no_key.append([i])
        else:
            print('WTFFFF')

    print(len(left))

    shuffle(no_key)

    no_key = no_key[len(left)*2:]  
    #print(len(no_key))


    df3 = []

    for i,f in enumerate(df[1]): 
        if [i] not in no_key:
            df3.append([df[0][i], df[1][i]])


    np.save('balanced_data-{}'.format(starting_value),df3)
    print('File {} finished!'.format(starting_value))
    


while True:
    file_name = 'firing_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        train_data = np.load('firing_data-{}.npy'.format(starting_value))
        print('File exists, moving along',starting_value)
        balance(starting_value,train_data)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)
        
        break
'''
ts = np.load('balanced_data-2.npy')

for data in ts:
    time.sleep(.2)
    img = (data[0])
    movement = data[1]
    #mouse = data[2]
    #mouse_click = data[3]
    print(movement)

    cv2.imshow('GamePlay',img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
'''