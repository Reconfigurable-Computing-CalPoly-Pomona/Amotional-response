# Low-Cost Embedded Animatronic, Emotion Detection

Senior Project 2019-20

Project repository for Dominic Holloman, Kevin Worsley

**Overview**

This project aims to produce an animatronic figure at low cost with a great deal of expressive potential. The device contains a fully embedded device design, using lights, sound, and simple motion to react to a user’s emotion,as expressed by their face. A convolutional  neural network trained to recognize four emotions is deployed, providing a level of interactivity often not seen in commercial products, particularly in the field of animatronics.

**Presentation Link: https://youtu.be/V8JK8axZZhU**

**Software**
* Files (Neural Network):
  * cnn-model-train.py : Training file for a convolutional neural network, training on the fer2013 dataset
  * dataset-load.py : Algorithm to take fer2013.csv and turn it into useful training format
  * image-inference.py : Runs a webcam object and performs inference with the model over its stream
  * keras-converter.py : Converts standard Tensorflow model format to TFLite for embedded device
  * pi-inference.py : Script for image collection and inference that runs on the Pi Zero W
  
* Files (Microcontrollers):
  * Demo_PIC18F4321_MainCode.C : This is the code from the presetation for the main microcontroller.
  * Demo_PIC12F1822_AudioCode.C : This is the code from the presetation for the microcontroller responsible for audio generation.
  
 **Pictures**
 * Files:
   * PCB.PNG : A screenshot of the current PCB layout.
   * SP_Render_Cropped.png : A 3D render of the current animatronic exterior.
  
**Hardware**
* Files:
  * SeniorProject.PCB : Current PCB design
  * SeniorProject.sch : Current schematic of hardware
  

**Supervising Professor:**

- Mohamed El-Hadedy: Assistant Professor, Electrical and Computer Engineering department, College of Engineering, California State Polytechnic University, Pomona.

**Collaborators:**

1. Wen-Mei Hwu: Director of Center for Cognitive Computing Systems Research and Walter J. Sanders III-AMD Endowed Chair Professor in Elecrical and Computer Engineering at UIUC

2. Jinjun Xiong: Director of Center for Cognitive Computing Systems Research and Adjunct Research Professor at UIUC
Electrical and Computer Engineering

California Polytechnic University, Pomona


--------------------------------------

**Model Information**

The model is a Convolutional Neural Network, trained on the fer2013 emotion dataset (3995 examples per emotion). The network passes information through a variety of convolutional modules, before being flattened and loaded into a decreasing net of densely-connected layers. The input data is augmented to improve its accuracy in a real world environment. 

**Hardware Information**

The hardware are designed using PIC microcontrollers from coursework at Cal Poly Pomona and provide sufficient IO control to manage the hardware peripherals dedicated to creating believable emotional responses. After an emotion is detected by the Convolutional Neural Network, the microcontrollers choose an appropriate reaction to the user's emotion and display that reaction with the peripherals.

<p align="center">
<img src="https://github.com/Reconfigurable-Computing-CalPoly-Pomona/Emotional-Response-Animatronic/Pictures/SP_Render_Cropped.png" >

	Figure 1: 3D Model of the Animatronic
</p>

--------------------------------------
