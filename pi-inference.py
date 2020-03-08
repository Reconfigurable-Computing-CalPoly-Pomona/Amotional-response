import time

start = time.time()
import cv2
import tensorflow as tf
import numpy as np
end = time.time()

print("[INFO] Imports completed in ", (end-start), '\n')

dimensions = (1,48,48,1)

NUM_CYCLES = 10

#cascade_data_loc = '/home/kevin-worsley/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
cascade_data_loc = '/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml'
save_dir = '/home/pi/photos_to_test/'

face_cascade = cv2.CascadeClassifier()
face_cascade.load(cascade_data_loc)

print("[SUCCESS] Haar Cascade detector loaded \n")

interpreter = tf.lite.Interpreter(model_path='cnn_emotion.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
#model_load = tf.keras.models.load_model('cnn_face_tolite.model')

print("[SUCCESS] TFLite Interpreter initialized \n")

for i in range(10):
    webcam = cv2.VideoCapture(0)
    print("Smile!")
    time.sleep(1)
    start_photos = time.time()
    success, frame = webcam.read()

    if(success):
        print("[SUCCESS] Frame " + str(i) + " captured at ", (time.time()- start_photos))
        webcam.release() #close the cam, we already took the photo
        filename = save_dir + 'testimage' + str(i) + '.jpg'
        cv2.imwrite(filename, frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(frame, 1.3, 5)  # finds the faces

        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            faceROI = frame[(y):y + (h), x:(x) + (w)]

        if (len(faces) != 0):
            print("   [SUCCESS] Found a face \n")
            image_resized = cv2.resize(faceROI, (48, 48), cv2.INTER_AREA)
            print("      [INFO] Image resize to ROI succeeded")

            image_to_model = np.reshape(image_resized, (1, 48, 48, 1))
            print("      [INFO] Image is reshaped for model")

            image_to_model = image_to_model.astype('float32') / 255.0  # tf.keras.utils.normalize(image_to_model, axis=0)
            print("      [INFO] Image is normalized")

            print(image_to_model.shape)
            print("      [INFO] Image ready to pass to model \n")

            start_detect = time.time()
            interpreter.set_tensor(input_details[0]['index'], image_to_model)
            interpreter.invoke()

            result = interpreter.get_tensor(output_details[0]['index'])
            print(result)
            emotion = np.argmax(result)
            end_detect = time.time()

            if(emotion ==0):
                print("     [RESULT] Face is angry \n")
            elif(emotion == 1):
                print("     [RESULT] Face is happy \n")
            elif(emotion == 2):
                print("     [RESULT] Face is sad \n")
            elif(emotion == 3):
                print("     [RESULT] Face is neutral \n")
            else:
                print("[ERROR] Unreachable point in code, should not trigger")

            print("[INFO] Operation took ", (end_detect-start_detect), "\n\n\n\n\n\n")
        else:
            print("   [FAIL] Could not find a face \n")






    else:
        print("[FAIL] Frame did not open")

print('[INFO] Exiting...')
cv2.destroyAllWindows()
