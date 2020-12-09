
This readme explains how the training data for the vehiclelanedetection neural network was retrieved

The training data is saved as newLabelData2 and newTrainingData2 as pickle files with protocol 3
The other versions are the same but saved with pickle protocol 2.
Execute the steps in python 2.7 unless sated otherwise

Step 1: Run The SaveData file, make sure you have selected a directory with bag files in the file.
		This runs a slow neural network that detect lanes in the images, but it is too slow for practical use.
		That is why extract just the labeled lines and use it to train a new simplified neural network,
		as the old network did more labeling than we needed which slowed it down.

Step 2: As rosbag is still not compatible with python 3 the files have to be saved in pickle with protocol 2
		As we train the network in python 3, we use the convertData file with a python 3.6 interpreter to rewrite the files to pickle
		protocol 3
		
Step 3: Run the neural network with python 3.6 interpreter, with the files created with the convertData file.

Improvements: Using the neural network to make training data is not optimal as it takes a lot of time and it 
is very sensitive to change in saturation in the image, in some cases not labeling the lanelines at all.
A better method would be some automatic lane detector or to manually label lines for a more accurate perfomance 
of the new neural network or you could try to edit the saturation in images to the old neural network so
it actually sees lines more often.

