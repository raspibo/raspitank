#!/usr/bin/python
import os
import wiringpi2 as wiringpi
import curses
import time
import sys
import threading
class getkey(threading.Thread):
	key = ''
	light = False
	motion = 'stop'
	direction = 'straight'
	mstr = ['stop ','stop ','stop ','stop ','stop ']
	def run(self):
		while self.key != 27:
			self.key = stdscr.getch()
			if self.key == ord(' '): #spazio accende e spegne le luci
				if self.light:
					motor.digitalWrite(11,motor.LOW)
					time.sleep(0.5)
					self.light = False
					stdscr.addstr(6,5,"Lights:off")
				else:
					motor.digitalWrite(11,motor.HIGH)
					time.sleep(0.5)
					self.light = True
					stdscr.addstr(6,5,"Lights:on ")
			elif self.key == curses.KEY_HOME or self.key == curses.KEY_END: #HOME accende lo stream, END accende lo stream notturno
				self.videostart = os.system("ps -ae|grep raspivid > /dev/null")
				if self.videostart !=0:
					stdscr.addstr(7,5,"Stream:on USE nc raspitank.local 9999 |mplayer -fps 150 -demuxer h264es -")
					if self.key == curses.KEY_HOME:#-sa e' la saturazione
						os.system('raspivid -t 0 -fps 15 -w 640 -h 480 -ex antishake  -o - |nc -l 9999 &')
					else:
						os.system('raspivid -t 0 -fps 15 -w 640 -h 480 -ex night  -o - |nc -l 9999 &')
				else:
					stdscr.addstr(7,5,"Stream:off                                                                 ")
					os.system('killall raspivid >/dev/null')
					os.system('killall nc >/dev/null')
			elif self.key == curses.KEY_UP: #FRECCE muovono il robot
				if self.motion == 'back':
					stop()
					self.motion = 'stop'
					time.sleep(0.2)
				elif self.motion == 'stop':
					avanti()
					self.motion = 'forward'
			#	stdscr.addstr(2,5,"Motion:"+self.motion+"    ")
			#	stdscr.refresh()
			elif self.key == curses.KEY_DOWN:
				if self.motion == 'forward':
					stop()
					self.motion = 'stop'
					time.sleep(0.2)
				elif self.motion == 'stop':
					indietro()
					self.motion = 'back'
			#	stdscr.addstr(2,5,"Motion:"+self.motion+"    ")
			#	stdscr.refresh()
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
			#	stdscr.refresh()
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
			#	stdscr.addstr(2,5,"Motion:"+self.motion+"    ")
			#	stdscr.addstr(3,5,"Direct:"+self.direction+"         ")
			#	stdscr.refresh()
			elif self.key == ord('a'):
				arm(0,True)
			elif self.key == ord('q'):
				arm(0,False)
			elif self.key == ord('s'):
				arm(4,True)
			elif self.key == ord('w'):
				arm(4,False)
			elif self.key == ord('d'):
				arm(2,True)
			elif self.key == ord('e'):
				arm(2,False)
			elif self.key == ord('f'):
				arm(3,True)
			elif self.key == ord('r'):
				arm(3,False)
			elif self.key == ord('z'):
				arm(1,True)
			elif self.key == ord('x'):
				arm(1,False)
			elif self.key == 263:
				stop()
				self.motion = 'stop'	
			stdscr.addstr(3,5,"Motion:"+self.motion+"    ")
			stdscr.addstr(4,5,"Direct:"+self.direction+"         ")
			stdscr.addstr(5,5,"Motor1:"+self.mstr[0]+" Motor2:"+self.mstr[4]+" Motor3:"+self.mstr[2]+" Motor4:"+self.mstr[3]+" Motor5:"+self.mstr[1])
			stdscr.refresh()
		exit()

def arm(armot,updn):
	stop()
	getkey.motion = 'stop'
	for mtr in motors:
		if mtr[0] != motors[armot][0]:
			mtr[1] = 0
	if motors[armot][1] == 0 and updn:
		motors[armot][1] = 1
		avanti()
		motor.digitalWrite(motors[armot][0],motor.HIGH)
		if armot == 0:
			getkey.mstr[0] = 'close'
		elif armot == 1:
			getkey.mstr[1] = 'right'
		else:
			getkey.mstr[armot] = 'down '		
	elif motors[armot][1] == -1 and updn:
		motors[armot][1] = 0
		stop()
	elif motors[armot][1] == 0 and not updn:
		motors[armot][1] = -1
		indietro()
		motor.digitalWrite(motors[armot][0],motor.HIGH)
		if armot == 0:
			getkey.mstr[0] = 'open '
		elif armot == 1:
			getkey.mstr[1] = 'left '
		else:
			getkey.mstr[armot] = 'up   '
	elif motors[armot][1] == 1 and not updn:
		motors[armot][1] = 0
		stop()
	else:
		motors[armot][1] = 0
		stop()

def orario():
	servostart("echo 0=50 > /dev/servoblaster")
def indietro():
	motor.digitalWrite(10,motor.HIGH)
def avanti():
	motor.digitalWrite(12,motor.HIGH)
def stop():
	motor.digitalWrite(10,motor.LOW)
	motor.digitalWrite(12,motor.LOW)
	motor.digitalWrite(5,motor.LOW)
	motor.digitalWrite(6,motor.LOW)
	motor.digitalWrite(4,motor.LOW)
	motor.digitalWrite(3,motor.LOW)
	motor.digitalWrite(14,motor.LOW)
	getkey.mstr = ['stop ','stop ','stop ','stop ','stop ']
def antiorario():
	servostart("echo 0=250 > /dev/servoblaster")
def dritto():
	servostart("echo 0=135 > /dev/servoblaster")
def servostart(strserv):
	motor.digitalWrite(8,motor.HIGH)
	os.system(strserv)
	time.sleep(0.5)
	motor.digitalWrite(8,motor.LOW)

motor = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
motor.pinMode(10,motor.OUTPUT) 
motor.pinMode(12,motor.OUTPUT)
motor.pinMode(13,motor.OUTPUT)
motor.pinMode(8,motor.OUTPUT)
motor.pinMode(11,motor.OUTPUT) 
motor.pinMode(5,motor.OUTPUT) 
motor.pinMode(6,motor.OUTPUT)
motor.pinMode(4,motor.OUTPUT)
motor.pinMode(3,motor.OUTPUT)
motor.pinMode(14,motor.OUTPUT)
stop()
dritto()
if __name__=="__main__":
	if os.system("ps -ae |grep servod > /dev/null") !=0:
		os.system("sudo ./servod --p1pins=7 > /dev/null")
	stdscr = curses.initscr()
	curses.cbreak()
	curses.noecho()
	curses.curs_set(0)
	stdscr.keypad(1)
	motors = [[6,0],[5,0],[4,0],[3,0],[14,0]]
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
#			link = os.popen('iwconfig wlan0 |grep "Link Quality"') #deprecated
			link = os.popen('cat /proc/net/wireless |tail -1|cut -c 13-18')
#			linkq.clear()
			linkq.addstr(0,0,"Link Quality"+link.read())
			linkq.refresh()
			#stdscr.addstr(15,5,link.read().strip())
			#stdscr.refresh()
			secondpass = time.time()
	os.system('killall raspivid >/dev/null')
	os.system('killall nc > /dev/null')
	stop()
	curses.endwin()
	motor.digitalWrite(11,motor.LOW)
