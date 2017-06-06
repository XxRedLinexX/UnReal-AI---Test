import numpy as np
import pandas as pd
import cv2

#train_data = np.load('training_data-1.npy')
train_data = np.load('firing_data-7.npy')

df = pd.DataFrame(train_data)

#for i in df[1]:
#    print(i)


for data in train_data:
    img = data[0]
    #movement = data[1]
    #mouse = data[2]
    #mouse_click = data[3]
    #print(movement)

    cv2.imshow('GamePlay',img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
