import time
import Adafruit_BBIO.GPIO as GPIO
from third_party_solver.enums import Color as Side

# setp, dirrection
motor_pins = {  Side.R: ("P2_25", "P2_27"),
				Side.U: ("P2_22", "P2_24"),
				Side.F: ("P2_18", "P2_20"),
				Side.D: ("P2_17", "P2_19"),
				Side.L: ("P2_9",  "P2_11"), 
				Side.B: ("P2_6", "P2_8")
}
	

for side in motor_pins.keys(): #[Side.R, Side.U, Side.F, Side.D, Side.L]:
	step, direction = motor_pins[side]
	GPIO.setup(step, GPIO.OUT)
	GPIO.setup(direction, GPIO.OUT)

def turn90(side, cw, switch):
	step, direction = motor_pins[side]
	if cw:
		GPIO.output(direction, GPIO.HIGH)
	else:
		GPIO.output(direction, GPIO.LOW)
	for i in range(100):#range(200 + (10 if switch else 0)):
		# Ramp up and down the motor
		sleep_time = 0.005 #0.001 + 0.00005 * abs(i - (100 + (5 if switch else 0)))
		GPIO.output(step, GPIO.HIGH)
		time.sleep(sleep_time)
		GPIO.output(step, GPIO.LOW)
		time.sleep(sleep_time)
	#time.sleep(2)
		
cw = True
switch = True
for iii in range(4):
	for ii in range(2):
		print("Running 90 degrees " + ("cw" if cw else "ccw"))
		for side in motor_pins.keys():
			turn90(side, cw, switch)
		switch = False
	cw = not cw
	switch = True
	print("Switching dirrection")

	