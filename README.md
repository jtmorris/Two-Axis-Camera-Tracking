# Two-Axis Camera Object Tracking Project
<p align="center">
        <img src="resources/mechanism_in_action.gif">
</p>

*View of the tracking mechanism in action. Camera is tracking a suspended pink Post-It swinging behind the camera filming.*

## Theory and Methods
Utilizing a webcam and computer vision techniques, I sought to track an object in 3D space utilizing a two degree of freedom motorized mechanism. I opted to use the OpenCV computer vision library and Python 3 for computer vision. I opted for two stepper motors controlled by an Arduino and L298N dual H-bridge motor controllers. The communication between the computer (Python) and the Arduino would occur over a serial connection using mutually known flag characters (ASCII integers 1 through 4) sent from Python, over USB, to indicate which motor to move and and which direction.

This repository contains the Python and Arduino code written to execute this project. 

<p align="center">
        <img src="resources/camera_view.gif">        
</p>

*View from the camera being articulated to track a pink Post-It (top). A yellow circle is imposed around the contour of the detected object and a red dot is imposed indicating the calculated centroid of the contour. Additionally shown is the mask of the camera view containing the object to track after computer vision selection techniques have been applied (bottom).*

## Prerequisites
- A computer with Python 3, [NumPy](https://pypi.org/project/numpy/), OpenCV, and [imutils](https://pypi.org/project/imutils/) installed. Computer requires a USB port for camera input and a USB port for serial communication with Arduino. 
   - *(Project developed using OpenCV 4.1.0 on 64-bit XUbuntu 19.04 running Python 3.7.)*
- An Arduino microcontroller with at least 8 available digital output pins and a USB cable. 
   - *(Project used an Arduino Mega2560 R3.)*
- A USB video camera. 
   - *(Project used a Logitech C920 HD webcam.)*
- Two stepper motors. 
   - *(Project used generic Nema 17 motors.)*
- Two stepper motor controllers capable of interfacing with the Arduino Stepper.h library. 
   - *(Project used two L298N dual H-bridge motor controllers.)*
- 12 to 48 volt power source for driving motors and motor controller. 
   - *(Project used a DC power supply providing 24 volts.)*
- Electrical project basics, such as jump wires and breadboards.
- Sufficient motor linkages and connections. 
   - *(Project used 1/2 inch square dowel rods and relevant fasteners. (see pictures above and below))*

## Setup
### Computer
Specifics are highly variable, depending on your rig. This guide is largely similar to the setup procedure I used: https://web.archive.org/save/https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/. I installed XUbuntu 19.04 on an external hard drive connected to my Microsoft Surface Pro 3, then executed installation of OpenCV and requisites largely recreating the steps outlined in that article with the following caveats and adjustments.

In step 4, I used the following cmake command:
```shell
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \                                    
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D INSTALL_PYTHON_EXAMPLES=ON \
        -D INSTALL_C_EXAMPLES=ON \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D OPENCV_EXTRA_MODULES_PATH=\~/opencv_contrib/modules \
        -D PYTHON_EXECUTABLE=\~/.virtualenvs/cv/bin/python \
        -D BUILD_EXAMPLES=ON \
        -D BUILD_DOCS=ON \
        -D OPENCV_GENERATE_PKGCONFIG=ON ..
```
 
pkg-config check at the end of step 4 will fail. Everything works anyway, so don't worry about it. Just skip it.
 
 
In step 5, with (X)Ubuntu 19.04, the path is `/usr/local/lib/python<*your version here*>/site-packages/cv2/python-<*your version here*>/`, not `/usr/local/python/cv2/python-3.6`.

### Arduino
- Wire stepper motors to Arduino and power supply to motor controllers. (Handy starter guide to motor wiring if you're unfamiliar: https://web.archive.org/web/20190725070024/https://www.makerguides.com/l298n-stepper-motor-arduino-tutorial/)
- Edit the *serial_triggered_control.ino* code to reference the digital pins you wired to and motor variables.
   - Relevant variables are near top of file, named STEPPER_<*motor plane*>_<*pin #*>.
   - If different stepper motors are used, STEPPER_STEPS_PER_REV as well as STEPPER_SPEED may also need adjusting.
- Compile and upload the Arduino script *serial_triggered_control.ino* to your Arduino.
- Leave Arduino plugged into your computer via USB to enable serial communication necessary for motor control.

### Mechanism Setup
<p align="center">
        <img src="resources/mechanism_close_up.jpg">        
</p>

The idea is to have a horizontal plane of tracking controlled by one motor. The output shaft of that motor is attached to a second motor controlling the vertial plane of tracking. Attached to that motor output shaft is the camera. I simply used short pieces of 1/2 inch wooden square dowel rod press fit onto each motor shaft via drilled holes. The vertical plane motor was then attached to the horizontal output shaft dowel using machine screws through the dowel into the motor mount points. The camera was mounted to the vertical plane output shaft dowel using a [setup stud](https://www.mcmaster.com/90281a095) with threads matching the camera tripod attachment fitting.

Any number of modifications or alterations can be made. You simply need the motors controlling 2-axes of rotation independently, one parallel to the camera FOV orientation, one perpendicular to the camera FOV orientation.

### Computer Vision Setup
In its current state, the program tracks a [pink Post-It](https://amzn.to/2Yb1Oby), as it was easily distiguishable from the background where I tested. Detection is done using a range of HSV colors determined through experimentation to match colors in my specific lighting conditions while narrow enough to reject false positives. You will likely need to experiment to detect the object you wish to detect. Specifics are highly variable to your circumstances and desires.

OpenCV finds the mask of objects you want and determines appropriate action in *camera_tracker.py*. Have fun.

## Running the Project
Once everything is setup and on, the tracking is initiated by feeding *camera_tracker.py* to the Python 3 interpreter.
Example from Linux terminal within working directory containing files:
```shell
$ python3 camera_tracker.py
```

The *camera_tracker.py* script accepts 4 arguments.

- **-c / --camera_index**: If using a Linux or Mac system, USB cameras are accessed by "/dev/video<*camera index #*>". This argument is that index #. By default, the script assumes camera index 0 (/dev/video0). If your system has multiple cameras, you may need to reference a different device. If using Windows or some other system, the webcam stream code will need to be altered to use appropriate formatting and notation.
- **-w / --processing_width**: Manually override the default frame size used for processing object detection. Larger frames offer more space and higher quality, but require more processing power. Lowering this number will yield faster results. By default, it is 800 pixels, which was determined to yield 30 to 40 frames per second on my computer with displaying of each frame and the detected mask each iteration.
- **-x / --resolution_width**: The resolution width to retrieve from the USB camera. Higher resolutions (e.g. full 1080p) require more processing power and are unnecessary if the processing width dramatically decreases the resolution. Most cameras only function at certain resolutions, and will error out if different resolutions are requested. My Logitech C920 feeds 960x540, among others, which is decently sized input and not substantially higher than the resized width for processing. You may need to specify an appropriate resolution. Defaults to 960.
- **-y / --resolution_height**: The height corresponding to the above *--resolution_width*. Same caveats apply. Defaults to 540.

Two examples from Linux terminal within working directory containing files specifying all 4 arguments using shorthand and longhand notation.
```shell
$ python3 camera_tracker.py --camera_index 4 --processing_width 800 --resolution_width 960 --resolution_height 540

$ python3 camera_tracker.py -c4 -w800 -x960 -y540
```

You will likely want to tweak argument defaults, defined within *camera_tracker.py*, to suit your situation once you've determined optimal conditions. Defaults are setup to match my situation and likely won't work for you out of the gate.

---

## Identified Potential Future Improvements
- My vertical plane Nema 17 stepper motor is underpowered for the webcam I use. In certain orientations, the motor is overpowered by the torque exerted on the output shaft. In most other orientations, the motor is sluggish to respond and occasionally misses steps. A slightly larger and more torque capable Nema 17 would improve performance.
- Stepper motors do not have fluid motion at low speed with full steps. A microstep-capable motor controller and/or acceleration ramping and other jerk limiting control code would make my rig less jerky, noisy, and spastic.
- Servo motors would be a better choice of motor for more fluid motion. Tracking is already practically limited to a FOV in front of the camera's setup position, due to attached wires. A limited range-of-motion servo would suffice, and would keep camera within position limits. Stepper motors have the advantage of known angle change by number of steps. As this project implements feedback control from the camera, a known angle change is irrelevant. Traditional electric or servo motors would be a better choice. I simply had sufficiently sized steppers on hand.
- When depowered, the motors do not hold position, and the camera is prone to rotating to a random position based on its center of gravity and any wire tension at power down. Typically, this means pointing straight down to the surface it is mounted to. This means the camera usually must be manually pointed in the desired direction, before powering up the motors and starting the program. Ideally, some logic (and possibly feedback control) would be implemented to lift the camera into desired position automatically upon application of power and control.
- More complex or intelligent object detection than "I see pink blob" would be preferable. At a minimum, some sort of checker pattern detection. The pink Post-It option is limiting, highly dependent upon lighting conditions and background. However, it was a simple starting point.
- The Arduino microcontroller is the bottleneck of this project. Motor control is handled by passing of characters over a serial connection (extremely slow). The Arduino code, as is, uses blocking motor control. The Arduino is slow on its own. Removing the Arduino middleman and utilizing GPIO native to the machine would be a more optimal solution. Either with a Raspberry Pi, or other project microcomputer with built-in GPIO, or with some USB GPIO adapter (e.g. [Adafruit FT232H Breakout](https://web.archive.org/save/https://www.adafruit.com/product/2264)).
- Mobility is wildly impractical with the setup I have. A bulky DC power supply, a sizable Surface Pro 3 connected to an external powered, external hard drive, with temporarily wired Arduino and L298N motor controllers makes it a fairly stationary, untransportable affair. A sufficient battery power source, computer utilizing built-in storage, removal of the Arduino (see previous list item), and more permanent wiring would allow this to be transported around to work in different areas.

## What I Learned With This Project / What Headaches Did I Have
- I had used OpenCV before with other projects; however, I [installed via pip](https://pypi.org/project/opencv-python/) rather than compiling from source. Compiling from source on Linux is not a new concept for me at all; however, I had to learn some specifics for compiling OpenCV specifically. Notably, getting it to play nice with Python 2 and 3.
- I learned a few tricks for object detection within an image regarding blurring, eroding, and dilating to eliminate false positive and artificating. https://www.pyimagesearch.com/ is one of several great resources that helped me net improved object detection. I initially tracked a green Post-It, and would get artifacts from shadows cast on the background wall and wall hangings before blurring, eroding, and dilating as I did in the end. A pink Post-It was less prone to false positives; however, I kept in a softened version of the mask alterations anyway.
- I initially attempted to execute this project in a Linux virtual machine using VirtualBox on my Windows desktop PC. Many, many problems ensued with getting the webcam to work at all, and the throughput made for an abysmal framerate. Don't bother with a virtual machine if your camera gives you any headaches. Stick with the bare metal. A Raspberry Pi would work well, though compilation of OpenCV takes a long time. I opted for my quite speedy Surface Pro 3 tablet.
- OpenCV uses a strange scale variant of the HSV color space, different from other software scales I've encountered. Coupled with the BGR, rather than RGB color space, it took longer to determine suitable HSV color ranges for masking than I would have preferred because of the need to convert, transpose, and rectify scales and systems. While simple enough, it was the most annoying part of the project beyond VirtualBox.
   > "For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]. Different softwares use different scales. So if you are comparing OpenCV values with them, you need to normalize these ranges." 
   > \- [OpenCV Docs](https://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html)
- I learned about myself that I don't have much desire for pink objects laying about in my space. Made for convenient object detection with a pink Post-It.
