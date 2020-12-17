# autonomousdrone

This is a high school project where I delved into drone building and optimization of its use cases through an attempt to add an element of autonomy.

The goal of the project is to produce a simple drone with manual controls then take it a step further with the ability to detect objects and return information about them – such as what they are and where they are. The drone built will be a 250 quadcopter and the tech specs are available in the documentation pdf. The object detection and data processing features will be running on a Raspberry Pi model 3 B+.

![Here is an idea of the scope that the system currently covers:](https://github.com/selin-k/autonomousdrone/blob/main/Picture1.png)
[a link](https://github.com/user/repo/blob/branch/other_file.md)

Regarding Object detection:

The CNN model used is a Caffe ([A deep learning framework](https://github.com/BVLC/caffe/)) [version](https://github.com/Zehaos/MobileNet) of the original [TensorFlow implementation](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet_v1.md) of the MobileNet SSD architecture. It was trained by [chuanqi305](https://github.com/chuanqi305/MobileNet-SSD). Upon training with the COCO dataset up to 20 objects can be detected by the drone with a mean average precision of 72.7%.

Here is some videos produced in the duration of this project:
[![autonomous-drone](https://github.com/selin-k/autonomousdrone/blob/main/Capture.PNG)](https://youtube.com/playlist?list=PL0nruMdk2V1aes5Wy8y1fI9kRXtD_ExmT)

My scope briefly, was a ‘seeing’ autonomous drone. The way I thought of it and structured my solution consisted of letting a Python script control the drone (using DroneKit) instead of me and getting it to perform a task for me such as detect the objects surrounding it and letting me know about it then doing something else – like landing if you see a person ahead.
The code for that Python script is [here](https://github.com/selin-k/autonomousdrone/blob/main/code/object-detection.py).
Feel free to criticize or offer suggestions. I will continue adding features and upgrade this drone with time.
