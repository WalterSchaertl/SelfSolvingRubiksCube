# Tests a motor-encoder pair, can be an automated test with correct set up
# This functionality will be integrated directly into Motors class

import Adafruit_BBIO.GPIO as GPIO
import Motors
import time

from third_party_solver.enums import Color as Side


def main():
    # Pocket Beagle's 4-channel stepper motor and 2-channel encoder
    side = Side.U#R
    motor = Motors.Motors(select=[side], sleep_time=0.001, debug=True).get_motor_by_side(side)
    margin_of_error = 5
    turns = [(-90, 270), (90, 0), (180, 180), (-180, 0)]
    for turn, actual in turns:
        motor.turn(abs(turn), True if turn > 0 else False)
        encoder_angle = motor.get_encoder_angle()
        if encoder_angle > actual - margin_of_error and encoder_angle < actual + margin_of_error:
            print("Observed value " + str(encoder_angle) + " tracks to " + str(actual) + ".")
        else:
            print("Encoder outside of tollerance! " + str(actual) + " vs " + str(encoder_angle))
        time.sleep(1)
        motor.reset()
        motor.encoder_angle = actual
            

if __name__ == "__main__":
    main()