# Tests if all the motors can be turned, encoder feedback not included yet,
# so no automatic pass/fail. Requires some setup, see the Motors class motor_pins
# dictionary for the pin assignments. Note that they should be in the same order
# as they're listed. If the motor turns the opposite dirrection it's suposed to, 
# reverse the wiring (or the pin order in motor_pins).

from third_party_solver.enums import Color as Side
from Motors import Motors

def main():
	print("Running Motor test, visual confirmation.")
	motors = Motors() 
	for side in Side:
		motors.turn_motor(side, 360, True)
	print(" Done.")

if __name__ == "__main__":
	main()