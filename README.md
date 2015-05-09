# Visual Alarm
Simple project for Raspberry Pi that toggles two LEDs based on a schedule. The utility will turn on the first light at "onTime" (set via command line arguments)will turn that light off and turn on the second light at "toggleTime" and turn both lights off at "offTime".


To use the Raspberry Pi device code, you must first install the GPIO module:
```
$ wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.1.0.tar.gz
$ tar zxf RPi.GPIO-0.1.0.tar.gz
$ cd RPi.GPIO-0.1.0
$ sudo python setup.py install
```
This also assumes you have wired up two LEDs.


An example command to run the tool is:
```
python visual_alarm.py -l1 18 -l2 22 -on 19:00 -toggle 21:00 -off 23:00
```
This will turn the LED wired to pin 18 on at 19:00. At 21:00, it will turn off pin 18 and turn on pin 22 and at 23:00 it will turn both pins off.


TODO:
* restful interface for toggling lights
* Android app to call rest API
