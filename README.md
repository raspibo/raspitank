This script interfaces a Raspberry Pi to an OWI arm joined with a GI Joe battle tank. Just remove the LED cable from the OWI motor board and put it directly on the RPi. Plug the tank motor in the former LED slot.
Through the RPi serial port this script sends commands to an ATmega8 that acts like a multiplexer. The ATmega8 switches relays linked to: OWI arm battery (it inverts polarity when activated), every single motor (5 in the arm, 1 in the tank) and a servo used for steering.
In the future, the ATmega8 could be used to interface some sensors.

Servoblaster's servod daemon executable must be in main folder. Otherwise you should modify 
	os.system("sudo ./servod --p1pins=7 > /dev/null")
with proper path.

This script works with GPIO's pins so it has to be run with sudo.

Arduino sketch raspitank.ino must be placed in the sketchbook.

You need to flash the sketch on an ATmega8 clocked no more than 4Mhz otherwise the serial port won't work.

You can find images at http://www.raspibo.org/wiki/index.php/RaspiTank
