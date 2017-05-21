import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

train_data = np.load("training_output.npy")
print(len(train_data))
df = pd.DataFrame(train_data)
print(Counter(df[1].apply(str)))

up = []
down = []
still = []

shuffle(train_data) #shuffle training data (it does not have to be linear)

for data in train_data:
    for data in train_data:
        img = data[0]
        key_input = data[1]

        if key_input == [1,0,0]:
            up.append([img, key_input])
        elif key_input == [0,1,0]:
            down.append([img, key_input])
        elif key_input == [0,0,1]:
            still.append([img, key_input])

up = up[:len(down)][:len(still)]
down = down[:len(up)][:len(still)]
still = still[:len(up)][:len(down)]

final_data = up + down + still

shuffle(final_data)
print(len(final_data))
np.save('training_output_v2', final_data)

#for data in train_data:
#    img = data[0]
#    key_input = data[1]
#    cv2.imshow('test',img)
#    print(img.shape)
#    print(key_input)
#    if cv2.waitKey(25) & 0XFF == ord('q'):
#        cv2.destroyAllWindows()
#        break
