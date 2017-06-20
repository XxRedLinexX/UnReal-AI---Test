import numpy as np
import pandas as pd
import cv2
import time
from random import shuffle
import os

starting_value = 1
remove = [296,283,274,162,155,244]
count = 1
data = []


while True:
    file_name = 'balanced_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        if starting_value in remove:
            print('Removed a ho-{}'.format(starting_value))
            starting_value += 1
        else:
            train_data = np.load('balanced_data-{}.npy'.format(starting_value))
            df = pd.DataFrame(train_data)
            print('File exists, moving along',starting_value)
            starting_value += 1
            for i,f in enumerate(df[1]):
                data.append([df[0][i], df[1][i]])
                if len(data) == 1000:
                    np.save('data_set-{}'.format(count),data) 
                    data = []
                    print('Data_Set-{} Complete'.format(count))
                    count += 1


    else:
        print('The Left Overs',len(df))
        np.save('data_set-{}'.format(count),data) 
        break







'''
tst = np.load('data_set-1.npy')

for data in tst:
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