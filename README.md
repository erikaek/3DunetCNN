
# 3D U-Net Convolution Neural Network with Keras
## Background
Originally designed after [this paper](http://lmb.informatik.uni-freiburg.de/Publications/2016/CABR16/cicek16miccai.pdf) on 
volumetric segmentation with a 3D U-Net.
The code was written to be trained using the 
[BRATS](http://www.med.upenn.edu/sbia/brats2017.html) data set for brain tumors, but it can
be easily modified to be used in other 3D applications. 

## Installation
All required installations can be made using the provided Dockerfile as:

	docker build . -t 3dunetcnn:latest

Thereafter, clone the project and cd into the project directory:

	cd 3DunetCNN

The contructed docker image is entered using:

	NV_GPU=0 nvidia-docker run --security-opt seccomp=unconfined --rm -u $(id -u):$(id -g) -v $(pwd):$(pwd) -w $(pwd) -ti 3dunetcnn:latest /bin/bash

where NV_GPU is used to select the GPU to train with. After entering the /bin/bash you need to add the working folder to pythonpath by:

	export PYTHONPATH=${PWD}:$PYTHONPATH

Train the network using either train.py for the original 3D U-net and train_isensee2017.py for the improved version. These files are in the different folders for different data scenarios: brats, headneck and iseg. Instructions for downloading and preprocessing the data are provided in the corresponding folders. One example of initiating training on the brats data using the original 3D U-net can be seen below:

	python brats/train.py

Without using docker, follow the tutorial for the Brats data for installation and testing

### Tutorial using BRATS Data
See README in the brats folder

