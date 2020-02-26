import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.utils
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import SeparableConv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.utils import plot_model
#from tensorflow.keras.utils
#from tensorflow.keras.utils.vis_utils import plot_model
import pandas as pd
import numpy as np
import scipy

import pydot
import graphviz

import matplotlib.pyplot as plt
import time

BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001
MAXIMUM_SAMPLES = 3995
#MAXIMUM_SAMPLES = 5500

data_dir = '/home/kevin-worsley/PycharmProjects/tensorflow-tests/fer2013.csv'


def load_dataset(datapath):
    print("Dataset loading...\n")
    fer2013_raw = pd.read_csv(datapath) #create a dataframe with the raw data

    # dataFrame holding training data, sorted by emotion
    train_df = fer2013_raw[
        (fer2013_raw['Usage'] == 'Training') &
        ((fer2013_raw['emotion'] == 0) |
         (fer2013_raw['emotion'] == 3) |
         (fer2013_raw['emotion'] == 4) |
         (fer2013_raw['emotion'] == 6))]

    #train_df.info()
    #print(train_df.head())

    # dataFrame holding testing data, sorted by emotion
    test_df = fer2013_raw[((fer2013_raw['Usage'] == 'PublicTest') |
        (fer2013_raw['Usage'] == 'PrivateTest')) &
        ((fer2013_raw['emotion'] == 0) |
        (fer2013_raw['emotion'] == 3) |
        (fer2013_raw['emotion'] == 4) |
        (fer2013_raw['emotion'] == 6))]

    #get rid of the usage columns now that we sorted everything
    train_df = train_df.drop(columns='Usage')
    test_df = test_df.drop(columns='Usage')

    #get lists of the training and testing data
    emotion_train_raw = train_df['emotion'].to_list()
    ete_raw = test_df['emotion'].to_list()

    ptr_raw = train_df['pixels'].to_list()
    pte_raw = test_df['pixels'].to_list()

    #0 = angry, 3 = happy, 4 = sad, 6 = neutral
    #0 = angry, 1 = happy, 2 = sad, 3 = neutral

    #counts for each sample in the set
    etr_happy = 0
    etr_sad = 0
    etr_angry = 0
    etr_neutral = 0

    etr_adj = []  # et = emotion_train
    ptr_npholder = []

    # load the images and labels together in the same loop iteration to control it
    #check the emotion
    #check if the maximum number of samples is reached
    #if so, don't do anything more
    #if not, add the emotion and image to the lists for training
    for i in range(len(emotion_train_raw)):
        if(emotion_train_raw[i] == 0): #angry
            if(etr_angry < MAXIMUM_SAMPLES): #if we haven't exceeded the limit
                etr_adj.append(0) #add emotion to new list

                temp_np = np.fromstring(ptr_raw[i], dtype='int', sep=' ')  # create a temporary long numpy array
                newshape = np.reshape(temp_np, (48, 48))  # shape the temp into what we want
                ptr_npholder.append(newshape)  # add that temp to the list

                etr_angry += 1
        elif(emotion_train_raw[i] == 3): #happy
            if (etr_happy < MAXIMUM_SAMPLES):
                etr_adj.append(1)

                temp_np = np.fromstring(ptr_raw[i], dtype='int', sep=' ')  # create a temporary long numpy array
                newshape = np.reshape(temp_np, (48, 48))  # shape the temp into what we want
                ptr_npholder.append(newshape)  # add that temp to the list

                etr_happy += 1
        elif(emotion_train_raw[i] == 4): #sad
            if(etr_sad < MAXIMUM_SAMPLES):
                etr_adj.append(2)

                temp_np = np.fromstring(ptr_raw[i], dtype='int', sep=' ')  # create a temporary long numpy array
                newshape = np.reshape(temp_np, (48, 48))  # shape the temp into what we want
                ptr_npholder.append(newshape)  # add that temp to the list

                etr_sad += 1
        elif(emotion_train_raw[i] == 6): #neutral
            if(etr_neutral < MAXIMUM_SAMPLES):
                etr_adj.append(3)

                temp_np = np.fromstring(ptr_raw[i], dtype='int', sep=' ')  # create a temporary long numpy array
                newshape = np.reshape(temp_np, (48, 48))  # shape the temp into what we want
                ptr_npholder.append(newshape)  # add that temp to the list

                etr_neutral += 1

    #create numpy array out of the temporary list of images
    ptr_data = np.array(ptr_npholder)  # make sure the list is a numpy array
    ptr_data = ptr_data.astype('float32') / 255.0  # normalize data
    print("Loaded training images")

    #onehot all the training values
    etr_onehot = tf.keras.utils.to_categorical(etr_adj,num_classes=4)
    print("Loaded onehot training labels")

    # plt.imshow(ptr_data[10400],cmap=plt.cm.binary)
    # plt.show()

    #TESTING DATA, LABEL ASSIGNMENT
    ete_adj = []
    for i2 in range(len(ete_raw)):
        if(ete_raw[i2] == 0):
            ete_adj.append(0)
        elif(ete_raw[i2]==3):
            ete_adj.append(1)
        elif(ete_raw[i2]==4):
            ete_adj.append(2)
        elif(ete_raw[i2] == 6):
            ete_adj.append(3)

    ete_onehot = tf.keras.utils.to_categorical(ete_adj,num_classes=4)
    print("Loaded onehot testing labels")

    pte_npholder = []
    for x2 in range(len(pte_raw)):
        temp_np2 = np.fromstring(pte_raw[x2],dtype='int',sep=' ')
        newshape2 = np.reshape(temp_np2, (48,48))
        pte_npholder.append(newshape2)

    pte_data = np.array(pte_npholder)
    pte_data = pte_data.astype('float32')/ 255.0

    print("Loaded testing images \n")
    print("Angry images: ", etr_angry)
    print("Sad images: ", etr_sad)
    print("Happy images: ", etr_happy)
    print("Neutral images ",etr_neutral,"\n")

    print("Train Images (Data): ",ptr_data.shape)
    print("Train Emotions (Labels): ", len(etr_onehot))

    print("Test Images (Data): ", pte_data.shape)
    print("Test Emotions (Labels): ", len(ete_onehot),"\n")

    ts = etr_angry + etr_happy + etr_angry + etr_neutral
    print(ts)


    return ptr_data, np.array(etr_onehot), pte_data, np.array(ete_onehot), ts
#--------------------------------------------------------------------------------

#TODO: Upsample the lower ones by repeating data, may induce overfitting, probably not relevant cause face is already detected

train_data, train_labels, test_data, test_labels, train_size = load_dataset(data_dir) #dataset is loaded!
train_data = np.reshape(train_data, (train_size,48,48,1)) #CHANGE ME WHEN INPUT SIZE CHANGES
test_data = np.reshape(test_data, (5212,48,48,1))

data_generator = ImageDataGenerator(
    featurewise_center=False,
    featurewise_std_normalization=False,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

print("Creating model...")

model = Sequential() #sequential style model

#TODO: Determine a convenient module that can be repeated
#TODO: Try this architecture https://arxiv.org/pdf/1710.07557.pdf

#This architecture is based off of a paper by Arriaga, Ploeger, and Valdenegro

model.add(Conv2D(64, (3,3), input_shape=(48, 48, 1)))

model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.2))

model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.2))

model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.2))

model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.2))

model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same',activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.2))

model.add(Flatten())
#model.add(tf.keras.layers.Dense(4096, activation='relu'))
model.add(tf.keras.layers.Dense(2048, activation='relu'))
model.add(tf.keras.layers.Dense(1024, activation='relu'))
model.add(tf.keras.layers.Dense(512, activation='relu'))
#model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(16, activation='relu'))

model.add(tf.keras.layers.Dense(4, activation='softmax'))

adam = tf.keras.optimizers.Adam(lr = LEARNING_RATE)

model.compile(optimizer='adam', loss = 'categorical_crossentropy',metrics=['accuracy'])

print(model.summary(),"\n")
plot_model(model, to_file='model.png')

lr_reducer = tf.keras.callbacks.ReduceLROnPlateau(monitor='loss',factor=0.9,patience=3)
stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy',min_delta=0, patience=5,mode='auto')
checkpoint = tf.keras.callbacks.ModelCheckpoint('/home/kevin-worsley/PycharmProjects/tensorflow-tests/checkpoint.hd5', monitor='val_accuracy', verbose=1, save_best_only=True)

check = input("Ready to train? Press Y or y when ready")

start_time = time.time()

#validation_data will use the test set, does not affect the training data
model.fit_generator(
    data_generator.flow(train_data,train_labels,BATCH_SIZE),
    epochs= EPOCHS,
    #batch_size= BATCH_SIZE,
    shuffle= True,
    callbacks=[lr_reducer,stop_early,checkpoint],
    validation_data=(test_data,test_labels)
)

#todo: see if irrelevant
model.evaluate(test_data, test_labels)

end_time = time.time()

print("Model training took ", (end_time-start_time)/3600, " hours \n")

model.save('cnn_face.model')

print("Model saved as cnn_face.model!")