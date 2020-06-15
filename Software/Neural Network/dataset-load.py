import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt

#VALUES = 35887
TRAIN_VALUES = 21005
TEST_VALUES = 5212
VALUES = 10

#import the csv and get it into a pandas DataFrame
fer2013 = "/home/kevin-worsley/PycharmProjects/tensorflow-tests/fer2013.csv"
fer2013_raw = pd.read_csv(fer2013)
fer2013_raw.info()

train_df = fer2013_raw[ #dataFrame holding training data, sorted by emotion
    (fer2013_raw['Usage'] == 'Training') &
        ((fer2013_raw['emotion'] == 0) |
         (fer2013_raw['emotion'] == 3) |
         (fer2013_raw['emotion'] == 4) |
        (fer2013_raw['emotion'] == 6))]

#train_df.info()

test_df = fer2013_raw[((fer2013_raw['Usage'] == 'PublicTest') | #dataFrame holding testing data, sorted by emotion
                       (fer2013_raw['Usage'] == 'PrivateTest')) &
        ((fer2013_raw['emotion'] == 0) |
         (fer2013_raw['emotion'] == 3) |
         (fer2013_raw['emotion'] == 4) |
        (fer2013_raw['emotion'] == 6))]

#test_df.info()

#turn the dataFrame into a numpy array where it'll stay
train_np = train_df.to_numpy()
print(train_np.shape)

#ditto, for test data
test_np = test_df.to_numpy()
print(test_np.shape)
print("---------------------------------------------")

#set up arrays for data to fill in
emotion_train = np.zeros((TRAIN_VALUES,1,))
image_train = np.zeros((TRAIN_VALUES,48,48))

emotion_test = np.zeros((TEST_VALUES,1,))
image_test = np.zeros((TEST_VALUES,48,48))

for i in range(TRAIN_VALUES):
    new_image_train = np.fromstring(train_np[i][1],dtype=int,sep=" ")
    new_image_train = new_image_train.reshape(48,48)

    emotion_train[i] = train_np[i][0]
    image_train[i] = new_image_train

for x in range(TEST_VALUES):
    new_image_test = np.fromstring(test_np[x][1],dtype=int,sep=" ")
    new_image_test = new_image_test.reshape(48,48)

    emotion_test[x] = test_np[x][0]
    image_test[x] = new_image_test

plt.imshow(image_test[5], cmap=plt.cm.binary)
plt.show()