# BOOTS-GUI-Python
Rewrite of the original BOOTS GUI written in Java, rewritten in Python and functionalities revised. Original GUI written in Java in 2015; functions on the BOOTS drop camera have changed substantially since then, and NDST does not have access to original source code written by Highland Technologies staff (IP resides with them).

This updated version of the GUI is written in Python 3.7, based on Tkinter GUI framework. The GUI instantiates a multi-connection TCP client, which communicates with TCP server instances generated by Moxa NPORT 5150 devices in the BOOTS subsea can (or EPOD). The GUI is designed for the following functionalities:

1) Interfacing with BOOTS' ProXR relays, which are control all BOOTS' relay functions, and provide an analog to digital conversion of the Ground Fault monitoring data form the DTEC ground fault monitoring PCB (10 bit, 0-5V ADC).

2) Interfacing with the StellarTech Depth Sensor, which outputs a pressure value in PSI, which is then converted into meters-seawater (using a nomincal latitudte value of 48 degrees)

3) Interfacing with a Remote Ocean Systems (ROS) PT-10 pan and tilt unit, which provide the pan and tilt functionalities for the BOOTS' MiniZeus HD camera. Furthermore, the GUI supports joystick control of this device, and user selectable speed settings, within a range of values acceptable to the PT-10 controller.

4) Interfacing with an Arduino Nano board in the BOOTS EPOD, which measuring the temperature (Celsius degrees), humidity (%), and pressure (hPa) within the BOOTS EPOD, as well as monitoring the digital output of a BlueRobotics SOS Leak sensor (0-3.3V logic).

5) Interfacing with the SBG systems IMU in the BOOTS EPOD, to display heading data from this device, as well as to monitor tether turns. A 'zero turns' button is implemented to allow the user to ensure that turns are properly zeroed out at surface.

6) Timestamp all data, and log it to a .CSV for later browsing. 

The following functions of the original Java GUI have bene removed:

1) Logging of GPS data (handled by Hypack directly)

2) Logging of Altitude data (handled by Hypacke directly; original Imagenex Altimeter removed in 2023).

3) Logging of BOOTS pitch and roll (handled by Hypack directly).
