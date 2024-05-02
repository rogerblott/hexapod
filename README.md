This is a web-controlled hexapod robot that uses a Raspberry Pi Zero 2W as the master controller and a Pico as the slave controller.  The latter is coded in Arduino C/C++ and the master in Python3 and
runs headless.  

MASTER
The master processor handles the web interface and the leg coordination.  The idea is to add a camera etc on a rotating head at some point but for now it just takes instructions from the web client and
sends then to the movement part of the software to coordinate leg movement.  Writing this in Python was so much easier than in Arduino and it works pretty well.  The hexapod can sit, stand, and walk in
any direction, and also rotate.  It can also walk and rotate, i.e. do a smooth turn.  The web interface is pretty basic but allows customisation of the walk mode: two gaits are implemented (tripod and
wave), the step size, speed, heading and amount of turn can all be set, and a certain number of steps (forward or back) can be executed.  And, there is a halt button. 

SLAVE
The slave processor does the work of managing the servo outputs, and manages an I2C 'tree' of devices to gather and filter feet and other sensor data.  The master uses an I2C interface to send servo commands to
the Pico and request the sensor data.  At the time of writing (May 2024) the sensor part is not complete nor operational and the hexapod does not use any feedback from sensors.

POWER
The hexapod has a total of 18 servos configured as hip (xy), knee and ankle (z).  The stl files are contained in the repository along with pictures.  It uses 6 x 18650 3.7 V LiPo batteries connected in 
2S3P configuration to provide power for the servos and (later) the neopixels, and a single 18650 to power the logic.  The servo power supply is regulated by 4 step-down regulators connected in parallel



Still to develop in no particular order:
1  feet sensors
2  accelerometers to measure limb angles
3  accelerometer/gyro to measure body attitude
4  camera capture/streaming
5  ultrasonic radar
6  neopixel display
7  rotating head for camera
8  feet and limb sensor feedback software
9  body movement software
