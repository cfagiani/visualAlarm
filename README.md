# Visual Alarm
Simple project for Raspberry Pi that toggles two LEDs based on a schedule. The utility will turn on the first light at "onTime" (set via command line arguments)will turn that light off and turn on the second light at "toggleTime" and turn both lights off at "offTime".


To use the Raspberry Pi device code, you must first install the GPIO module:
```
$ wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.1.0.tar.gz
$ tar zxf RPi.GPIO-0.1.0.tar.gz
$ cd RPi.GPIO-0.1.0
$ sudo python setup.py install
```

The Flask module is also used for the RESTful interface. This can be installed via:
```
sudo pip install flask
```
The port on which the restful interface is exposed can be changed via the -p command line option. If no option is supplied, it defaults to port 8080. The interface binds to the 0.0.0.0 interface on the Pi so it will be accessible by other hosts on the same network as the Raspberry Pi. The API does NOT provide any security features so you should ensure it's only used on a trusted network.


The utility assumes you have wired up two LEDs. The docs directory contains a picture of one possible breadboard configuration.


An example command to run the tool is:
```
sudo python visual_alarm.py -l1 18 -l2 22 -on 19:00 -toggle 21:00 -off 23:00
```
This will turn the LED wired to pin 18 on at 19:00. At 21:00, it will turn off pin 18 and turn on pin 22 and at 23:00 it will turn both pins off.

The time values are all assumed to be the default timezone as configured on the Raspberry Pi (so if your timezone is in UTC, the on/off times must be set in UTC). Time values can be changed via a web interface (accessible by default at http://localhost:8080/control.html on the Raspberry Pi).

## To Do
* better API to set all 3 times at once
* better control interface
* API to add additional events
* Return timezone in Rest API so UI can render times in local timezone
* Pin Status API 
* Refactor code so there is a more logical way to access the 'engine' from the rest interface

