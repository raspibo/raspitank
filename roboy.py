#!/usr/bin/python
import os
import wiringpi2 as wiringpi
import curses
import time
import sys
import threading
import serial

class getkey(threading.Thread):
	key = ''
	light = False
	motion = 'stop'
	direction = 'straight'
	mstr = ['stop ','stop ','stop ','stop ','stop ']
	def run(self):
		while self.key != 27:
			self.key = stdscr.getch()
			if self.key == ord(' '): #space turns the LED on and off
				if self.light:
					pins.digitalWrite(11,pins.LOW)
					time.sleep(0.5)
					self.light = False
					stdscr.addstr(6,5,"Lights:off")
				else:
					pins.digitalWrite(11,pins.HIGH)
					time.sleep(0.5)
					self.light = True
					stdscr.addstr(6,5,"Lights:")
					stdscr.addstr(6,12,"on ")
			elif self.key == curses.KEY_HOME or self.key == curses.KEY_END: #HOME turns on the video stream, END turns on the video stream in night mode
				self.videostart = os.system("ps -ae|grep raspivid > /dev/null")
				if self.videostart !=0:
					stdscr.addstr(7,5,"Stream:on ")
					stdscr.addstr(8,5,"nc raspitank.local 9999 |mplayer -fps 150 -demuxer h264es -")
					stdscr.addstr(9,5,"nc raspitank.local 9998 |aplay")
					os.system('./audio.sh >/dev/null 2>&1 &')
					if self.key == curses.KEY_HOME: #alter the .sh for custom video settings
						os.system('./videoday.sh >/dev/null 2>&1 &')
					else:
						os.system('./videonig.sh >/dev/null 2>&1 &')
				else:
					stdscr.addstr(7,5,"Stream:off                                                                 ")
					stdscr.addstr(8,5," ".ljust(60))
					stdscr.addstr(9,5," ".ljust(60))
					os.system('killall raspivid >/dev/null')
					os.system('killall nc >/dev/null')
			elif self.key == curses.KEY_DOWN: #ARROWS do the movement
				if self.motion == 'forward':
					stop()
					self.motion = 'stop'
					time.sleep(0.2)
				elif self.motion == 'stop':
					avanti()
					self.motion = 'back'
			elif self.key == curses.KEY_UP:
				if self.motion == 'back':
					stop()
					self.motion = 'stop'
					time.sleep(0.2)
				elif self.motion == 'stop':
					indietro()
					self.motion = 'forward'
			elif self.key == curses.KEY_LEFT:
				stop()
				self.motion = 'stop'
				if self.direction == 'right':
					dritto()
					self.direction = 'straight'
					time.sleep(0.2)
				elif self.direction == 'straight':
					self.direction = 'left'
					orario()
				else:
					self.direction = 'left'
					time.sleep(0.2)
			elif self.key == curses.KEY_RIGHT:
				stop()
				self.motion = 'stop'
				if self.direction == 'left':
					dritto()
					self.direction ='straight'
					time.sleep(0.2)
				elif self.direction == 'straight':
					self.direction = 'right'
					antiorario()
				else:
					self.direction = 'right'
					time.sleep(0.2)
			elif self.key == ord('a'):
				arm(1)
			elif self.key == ord('q'):
				arm(-1)
			elif self.key == ord('s'):
				arm(2)
			elif self.key == ord('w'):
				arm(-2)
			elif self.key == ord('d'):
				arm(3)
			elif self.key == ord('e'):
				arm(-3)
			elif self.key == ord('f'):
				arm(4)
			elif self.key == ord('r'):
				arm(-4)
			elif self.key == ord('z'):
				arm(-5)
			elif self.key == ord('x'):
				arm(5)
			elif self.key == 263:
				stop()
				self.motion = 'stop'	
			stdscr.addstr(3,5,"Motion:"+self.motion+"    ")
			stdscr.addstr(4,5,"Direct:"+self.direction+"         ")
			stdscr.addstr(5,5,"Motor1:"+self.mstr[0]+" Motor2:"+self.mstr[1]+" Motor3:"+self.mstr[2]+" Motor4:"+self.mstr[3]+" Motor5:"+self.mstr[4])
			stdscr.refresh()
		exit()

def arm(armot):
	global motActive
	getkey.motion = 'stop'
	if motActive == armot:
		return
	if motActive == (-1*armot):
		motActive =0
		stop()
		return
	stop()
	motActive = armot
	if armot < 0:
		ser.write(polarity0)
		armot = -1*armot
	else:
		ser.write(polarity1)
	ser.write(motONs[armot-1])
	if motActive == 1:
		getkey.mstr[0] = "open "
	if motActive == -1:
		getkey.mstr[0] = "close"
	if motActive >=2 and motActive <=4:
		getkey.mstr[motActive-1] = "down "
	if motActive <=-2 and motActive >=-4:
		getkey.mstr[(-1*motActive)-1] = "up   "
	if motActive ==5:
		getkey.mstr[4] = "right"
	if motActive ==-5:
		getkey.mstr[4] = "left "

def orario():
	servostart("echo 0=50 > /dev/servoblaster")
def indietro():
	ser.write(polarity0)
	ser.write(motON)
def avanti():
	ser.write(polarity1)
	ser.write(motON)
def stop():
	ser.write(motOFF)
	time.sleep(0.01)
	for sercomm in motOFFs:
		ser.write(sercomm)
		time.sleep(0.01)
	getkey.mstr = ['stop ','stop ','stop ','stop ','stop ']
def antiorario():
	servostart("echo 0=250 > /dev/servoblaster")
def dritto():
	servostart("echo 0=135 > /dev/servoblaster")
def servostart(strserv):
	ser.write(servoON)
	os.system(strserv)
	time.sleep(0.5)
	ser.write(servoOFF)

pins = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
pins.pinMode(11,pins.OUTPUT)
ser = serial.Serial(port='/dev/ttyAMA0',baudrate=9600)
polarity0 = "0"
polarity1 = "1"
motON = "c"
motOFF= "d"
servoON = "e"
servoOFF= "g"
motONs = ["2","4","6","8","a"]
motOFFs = ["3","5","7","9","b"]
motActive = 0
ser.open()
stop()
dritto()
if __name__=="__main__":
	if os.system("ps -ae |grep servod > /dev/null") !=0:
		os.system("sudo ./servod --p1pins=7 > /dev/null") #put correct path for servod
	stdscr = curses.initscr()
	curses.cbreak()
	curses.noecho()
	curses.curs_set(0)
	stdscr.keypad(1)
	stdscr.addstr(0,5,"Press ESC to quit, up/down = Motion, left/right = Direct, space = Lights, BACKSPACE = stop")
	stdscr.addstr(1,5,"home = Stream, end = Night stream, q/a w/s e/d r/f z/x = Arm motors")
	stdscr.addstr(3,5,"Motion:")
	stdscr.addstr(4,5,"Direct:straight")
	stdscr.addstr(5,5,"Motor1:stop  Motor2:stop  Motor3:stop  Motor4:stop  Motor5:stop")
	stdscr.addstr(6,5,"Lights:off")
	stdscr.addstr(7,5,"Stream:off")
	stdscr.refresh()
	linkq = curses.newwin(3,80,10,5)
	getkey = getkey()
	getkey.start()
	key=''
	secondpass = time.time()
	while getkey.key != 27:
		if time.time() - secondpass > 1:
			link = os.popen('cat /proc/net/wireless |tail -1|cut -c 14-17')
			link = link.read()
			try:
				link = int(link)
				if (link < 32) :
					linkq.addstr(1,0,"ATTENZIONE",curses.A_BOLD)
				else:
					linkq.addstr(1,0,"                        ")
				if (link < 20) :
					stop()
			except TypeError:
				stop()
			linkq.addstr(0,0,"Link Quality "+str(link)+"%                                   ",curses.A_BOLD)
			linkq.refresh()
			secondpass = time.time()
	os.system('killall raspivid >/dev/null')
	os.system('killall nc > /dev/null')
	stop()
        ser.close()
	curses.endwin()
	pins.digitalWrite(11,pins.LOW)
