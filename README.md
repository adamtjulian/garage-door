# util-pi

The util-pi contains code to monitor a remote pi via apache. Apache contains .json file with the current status of the garage door. The lcd.service file runs the python service to display the current status of the garage door by monitoring the remote pi

Pin Connection for LCD display:

GND to 39
VCC to 2
SDA to 3
SCL to 5


# garage-pi

The garage-pi uses reed sensor to determine if garage is open/closed, and outputs the status to a .json file that can be consumed by other services. The service file runs in the background to continuously update the garage file.

Using reed sensor, connect to board using ground and pin 9 (ground) and 15 (GPIO 22).

All .service files go in /etc/systemd/system