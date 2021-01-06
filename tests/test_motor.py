# Tests if all the motors can be turned, encoder feedback not included yet,
# so no automatic pass/fail. Requires some setup, see the Motors class motor_pins
# dictionary for the pin assignments. Note that they should be in the same order
# as they're listed. If the motor turns the opposite direction it's supposed to,
# reverse the wiring (or the pin order in motor_pins).

from third_party_solver.enums import Color as Side
from Motors import Motors
import time 


def main():
	print("Running Motor test, visual confirmation.")
	motors = Motors()
	while True:
		for side in Side:
			motors.turn_motor(side, 360, True)
			time.sleep(1)
		time.sleep(3)
	print(" Done.")

if __name__ == "__main__":
	main()
