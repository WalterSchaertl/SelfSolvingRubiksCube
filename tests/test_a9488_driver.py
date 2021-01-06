import time
import Adafruit_BBIO.GPIO as GPIO
from third_party_solver.enums import Color as Side

# step, direction
motor_pins = {	Side.R: ("P2_29", "P2_31"),
				Side.U: ("P2_22", "P2_24"),
				Side.F: ("P2_18", "P2_20"),
				Side.D: ("P2_17", "P2_19"),
				Side.L: ("P2_9", "P2_11"),
				Side.B: ("P2_6", "P2_8")
			}


# Turn a side, no particular amount, just to see functionality
def turn90(side, cw):
	step, direction = motor_pins[side]
	if cw:
		GPIO.output(direction, GPIO.HIGH)
	else:
		GPIO.output(direction, GPIO.LOW)
	for i in range(100):
		sleep_time = 0.005
		GPIO.output(step, GPIO.HIGH)
		time.sleep(sleep_time)
		GPIO.output(step, GPIO.LOW)
		time.sleep(sleep_time)


def main():
	# Init pins
	for side in motor_pins.keys():
		step, direction = motor_pins[side]
		GPIO.setup(step, GPIO.OUT)
		GPIO.setup(direction, GPIO.OUT)

	clockwise = True
	# Run each motor 4 times
	for i in range(4):
		print("Running 90 degrees " + ("clockwise" if clockwise else "counterclockwise"))
		for side in motor_pins.keys():
			turn90(side, clockwise)
		clockwise = not clockwise
		print("Switching direction")

if __name__ == "__main__":
	main()
