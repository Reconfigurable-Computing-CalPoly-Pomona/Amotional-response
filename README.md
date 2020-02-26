## Low-Cost Embedded Animatronic, Emotion Detection

Senior Project 2019-20

Project repository for Dominic Holloman, Kevin Worsley

* Files:
  * cnn-model-train.py : Training file for a convolutional neural network, training on the fer2013 dataset
  * dataset-load.py : Algorithm to take fer2013.csv and turn it into useful training format
  * image-inference.py : Runs a webcam object and performs inference with the model over its stream
  * keras-converter.py : Converts standard Tensorflow model format to TFLite for embedded device
  
#Model information

The model is a Convolutional Neural Network, trained on the fer2013 emotion dataset (3995 examples per emotion). The network passes information through a variety of convolutional modules, before being flattened and loaded into a decreasing net of densely-connected layers. The input data is augmented to improve its accuracy in a real world environment. 


Advisor: Dr. Mohamed El-Hadedy

Electrical and Computer Engineering

California Polytechnic University, Pomona
