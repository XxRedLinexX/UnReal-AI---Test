import numpy as np
from models import sentnet_color_2d
from random import shuffle
import pandas as pd

# what to start at
START_NUMBER = 1

# what to end at
hm_data = 112

# use a previous model to begin?
START_FRESH = True #False

WIDTH = 160
HEIGHT = 280
LR = 1e-3
EPOCHS = 10
frame_count = 3
MODEL_NAME = 'sentnet_color_2d-try1'
EXISTING_MODEL_NAME = ''

model = sentnet_color_2d(WIDTH, HEIGHT,frame_count, LR, output=5)

if not START_FRESH:
    model.load(EXISTING_MODEL_NAME)

for i in range(EPOCHS):
    data_order = [i for i in range(START_NUMBER,hm_data+1)]
    shuffle(data_order)
    for i in data_order:
        train_data = np.load('data_set-{}.npy'.format(i))
        print('Running data_set-{}.npy'.format(i))
        
        df = pd.DataFrame(train_data)
        df = df.iloc[np.random.permutation(len(df))]
        train_data = df.values.tolist()

        train = train_data[:-100]
        test = train_data[-100:]

        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,3)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,3)
        test_y = [i[1] for i in test]

        model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), 
            snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)