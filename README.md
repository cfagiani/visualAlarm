# visualAlarm
Simple project for Raspberry Pi that toggles two LEDs based on a schedule. The utility will turn on the first light at "onTime" (set via command line arguments)will turn that light off and turn on the second light at "toggleTime" and turn both lights off at "offTime".


To use the Raspberry Pi device code, you must first install the GPIO module:
```
$ wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.1.0.tar.gz
$ tar zxf RPi.GPIO-0.1.0.tar.gz
$ cd RPi.GPIO-0.1.0
$ sudo python setup.py install
```
This also assumes you have wired up two LEDs.


TODO:
* restful interface for toggling lights
* Android app to call rest API
