import cv2
import dlib
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.utils
import pandas as pd
import numpy as np
import imutils
import matplotlib.pyplot as plt

model_loaded = tf.keras.models.load_model('cnn_face.model')
face_cascade_data = '/home/kevin-worsley/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
dimensions = (48,48)

face_cascade = cv2.CascadeClassifier()
face_cascade.load(face_cascade_data)

#start loop here
webcam = cv2.VideoCapture(0)

#image = cv2.imread('angry.jpeg',0) #reads image as grayscale if 0 is added as arg

#webcam capture loop
while(True):
    success, image = webcam.read()
    to_display = image

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(image, 1.3, 5) #finds the faces

    for(x,y,w,h) in faces:
        image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        faceROI = image[(y):y+(h), x:(x)+(w)] #-2 gets rid of the bounding box

    image_resized = cv2.resize(faceROI,dimensions, interpolation=cv2.INTER_AREA)

    image_to_model = np.reshape(image_resized,(1,48,48,1))

    image_to_model = image_to_model.astype('float32') / 255.0#tf.keras.utils.normalize(image_to_model, axis=0)

    #TODO: Don't let program fail to start if a face not found

    if(len(faces) != 0):
        print("Found a face")
    else:
        print("Could not find a face")

    predictions = model_loaded.predict(image_to_model) #include file to check out
    result = np.argmax(predictions)

    face_result = ''

    if(result == 0):
        print("Angry face")
        face_result = 'Angry'
    elif(result == 1):
        print("Happy face")
        face_result = 'Happy'
    elif(result == 2):
        print("Sad face")
        face_result = 'Sad'
    elif(result == 3):
        print("Neutral face")
        face_result = 'Neutral'
    else:
        print("Not identified correctly")

    cv2.putText(to_display, face_result, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)
    #cv2.rectangle(to_display,faceROI[0], faceROI[1], (255,0,0),2)

    cv2.imshow('Webcam', to_display)
    cv2.imshow('To model', image_resized)
    #cv2.imshow("Face ROI", faceROI)
    #cv2.imshow("What model got", image_resized)

    if(cv2.waitKey(1) == 27):
        break

webcam.release()
cv2.destroyAllWindows()

#plt.imshow(image_resized,cmap=plt.cm.binary)
#plt.show()
#face is now found and ready to be passed to the model!

#cv2.imshow('Face found', image_resized)
#cv2.waitKey(0)
#cv2.destroyAllWindows()