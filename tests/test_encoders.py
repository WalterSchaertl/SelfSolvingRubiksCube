# Tests a motor-encoder pair, can be an automated test with correct set up
# This functionality will be integrated directly into Motors class

import Adafruit_BBIO.GPIO as GPIO
import Motors
import time

from third_party_solver.enums import Color as Side


def main():
    # Pocket Beagle's 4-channel stepper motor and 2-channel encoder
    sides = [Side.U, Side.R]
    motors = Motors.Motors(debug=True)
    while True:
        print("-------")
        for side in Side:#sides:
            encoder_angle = motors.get_motor_by_side(side).get_encoder_angle()
            print("Side: " + str(side.name) + " : " + str(encoder_angle))
        time.sleep(2)
if __name__ == "__main__":
    main()