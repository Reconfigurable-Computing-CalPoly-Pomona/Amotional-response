import tensorflow as tf
import numpy as np

converter = tf.lite.TFLiteConverter.from_keras_model('cnn_face.model')
tflite_model = converter.convert()
open("cnn_face.tflite", "wb").write(tflite_model)