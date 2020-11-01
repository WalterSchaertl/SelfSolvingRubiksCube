from Cube import Cube
from third_party_solver.enums import Color as Side

def main():
	test_cube = Cube(enable_motors=True, debug=True)
	test_motor = test_cube.motors.motors[Side.R]
	for turn in [90] * 2:
		test_motor.turn(abs(turn), True if turn > 0 else False)
		encoder_angle = test_motor.get_encoder_angle()
		print("Turned Motor " + str(test_motor) + " " + str(turn) + " degrees, now reading " + str(encoder_angle) + " on the encoder.")

	
if __name__ == "__main__":
	main()