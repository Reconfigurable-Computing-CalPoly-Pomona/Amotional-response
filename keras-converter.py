import tensorflow as tf

model_to_convert = tf.keras.models.load_model('cnn_face_tolite.model')

converter = tf.lite.TFLiteConverter.from_keras_model(model_to_convert)
print("Converting standard to TFLite...")
tflite_model = converter.convert()
print("Done! Saving file...")
open("cnn_emotion.tflite", "wb").write(tflite_model)
print("File saved as cnn_face.tflite")
