# TNO Vehicle Lane Detection

This is a program to make a top down visualisation of lanes and vehicles on a road. 

This program is known to work on Ubuntu, mainly on 18.04, we can't guarentee the 
functioning of this program on other operating systems or ubuntu versions.

The program either takes live input from roscore or can load in a bag file which
contains dashcam footage and coordinates of other cars, it uses the following 
topics:

* /prius1/camera_front_center/image_raw/compressed
* /prius1/world_model/targets 

The program can also write coordinates of the lines to the bag for future use.
These coordinates are written to the topic:

* lane_coordinates 

## Getting Started / Installing

Make sure the Zip with the project files is downloaded and unzipped.
After unzipping, run the setup.sh found in the unzipped folder.

Running the setup.sh can be done by opening the folder in which it is stored in
the terminal and typing:

```
chmod +x setup.sh
```
(if that doesn't work, try "chmod +x ./setup.sh")

This will make it runnable, and then run it by simply typing:

```
./setup.sh
```
This may take a few minutes.

Once that is done, unzip the Zip called 'Executable.zip' found in the same folder as 
the setup.sh.

Things should be all setup now for running the program.


### Future development

For future development, if any changes are made to the code, these are not 
captured in the executable. To run the program with these changes, you must run 
the main.py. In order to run this, all the packages used in the development are 
required. These packages can be easily installed by running the setup_dev.sh
```
chmod +x setup_dev.sh
```
(if that doesn't work, try "chmod +x ./setup_dev.sh")

This will make it runnable, and then run it by simply typing:
```
setup_dev.sh
```
Which automatically installs all packages necessary to edit and run the program.

Then, open terminal and run:

```
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

Furthermore, Python 2.7 is used in this project and should also be installed,
instructions on how to do this can easily be found online.

To run the program using python navigate to the repository and to the 
location where the main.py file is stored. Once there run 
```
python main.py
```
or alternatively if the default python is not python2.7, run
```
python2.7 main.py
```

## Running

After unzipping the Executable.zip, go into 
../Executable/dist/main and run the 'main' executable.

If that does not work as intended,
open ../Executable/dist/main in the terminal and run the 'main' file 
manually to get the error message to see what went wrong. This can be done by 
typing 'main' in the terminal

```
../Executable/dist/main/main
```

### With prerecorded bag

When running the program, press the "Choose bag" button and select the bag you 
want to play. 
By navigating to "File" and then "Write to bag file and quit" you can save
all the previously seen coordinates to the bag file. These coordinates can later 
be retrieved using the rqt_bag command from a terminal window (while roscore is 
active in another terminal). This launches a GUI program that allows you to see 
all the topics in the bag. Additionaly it has functionality such as playing the
bag, skipping through the bag, looking at raw data and publishing the data 
while you play.

If you experience a massive delay between pressing the pause button and the 
program actually pausing, assign more CPU cores to the virtual machine or run 
the program on a machine that has Ubuntu as its native operating system.

### Live input

When running the program, press the "Live input", the listeners of the program
will scan for input from publishers. So, if a publisher is sending information,
it will be shown in the program.

In the program's current form writing to a bag file requires the bag file to be
specified. As this is only the case in the prerecorded input this functionality
would have to be adapted if you would like to write live data to a bag.


## Deployment

This product could for example be used to inspect the quality of the radar data
provided in the bag file or inspect the quality of the lane detection performed.
In the future the structure made in this product can be used in a bigger project
that has to use a world model containing coordinates for all vehicles in the 
radar's range and coordinates for the lines on the road.

## Built With

* [ROS](http://wiki.ros.org/melodic/Installation) - The package used for reading
 and writing data
* [PyQT](https://wiki.python.org/moin/PyQt) - Package for the GUI
* [OpenCV](https://opencv.org/) - Package used for image manipulation
* [Tensorflow](https://www.tensorflow.org/) - Package used for the Neural Network
* [Keras](https://keras.io/) - Package used as API for Tensorflow
* [PyInstaller](https://www.pyinstaller.org/) - Used for making the executable
* [Python 2.7](https://www.python.org/download/releases/2.7/) - Programming language

## Authors

* **Domantas Giržadas** - *Scrum master*
* **Floris Griep** - *Team member*
* **Isaac Lee** - *Team memberk*
* **Nils Kimman** - *Team member*
* **Ole ten Hove** - *Team member*
* **Tijs Rozenbroek** - *Team member*
* **Yousif Eldaw** - *Team member*
* **Floris van Wettum** - *Proxy product owner*

## License

MIT License

Copyright (c) 2019-2020 Yousif Eldaw, Domantas Giržadas, Floris Griep, Nils 
Kimman, Isaac Lee, Tijs Rozenbroek, Ole ten Hove, Floris van Wettum

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

* We'd like to thank Jan-Pieter Paardekooper for guiding the process and giving 
advice where necessary.
