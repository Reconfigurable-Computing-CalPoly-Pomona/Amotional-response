import time

start = time.time()
import cv2
import tensorflow as tf
import numpy as np
end = time.time()

print("Imports completed in ", (end-start))

dimensions = (1,48,48,1)
cascade_data_loc = '/home/kevin-worsley/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
#cascade_data_loc = '/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier()
face_cascade.load(cascade_data_loc)

print("Haar Cascade detector loaded")

interpreter = tf.lite.Interpreter(model_path='cnn_emotion.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("TFLite Interpreter initialized")

webcam = cv2.VideoCapture(0)

for i in range(10):
    success, frame = webcam.read()

    if(success):
        print("---------Frame captured-----------")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(frame, 1.3, 5)  # finds the faces

        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            faceROI = frame[(y):y + (h), x:(x) + (w)]  # -2 gets rid of the bounding box

        if (len(faces) != 0):
            print("Found a face")

            image_resized = cv2.resize(faceROI, (48, 48), interpolation=cv2.INTER_AREA)

            image_to_model = np.reshape(image_resized, (1, 48, 48, 1))

            image_to_model = image_to_model.astype('float32') / 255.0  # tf.keras.utils.normalize(image_to_model, axis=0)

            print(image_to_model.shape)
            print("Image ready to pass to model \n")

        else:
            print("Could not find a face \n")







    else:
        print("Frame did not open")

webcam.release()
cv2.destroyAllWindows()

