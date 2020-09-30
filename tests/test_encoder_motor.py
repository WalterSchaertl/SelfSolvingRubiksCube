# Tests a motor-encoder pair, can be an automated test with correct set up
# This functionality will be intergrated dirrectly into Motors class
import Adafruit_BBIO.GPIO as GPIO
import Motors
import time

from third_party_solver.enums import Color as Side
        
def main():
    # Pocket Beagle's 4-channel stepper motor and 2-channel encoder
    motor = Motors.Motors(select=[Side.R], sleep_time=0.001).get_motor_by_side(Side.R)
    margin_of_error = 5
    for turn in [-90, 90, 180, -180, 360, -360]:
        motor.turn(abs(turn), True if turn > 0 else False)
        encoder_angle = motor.get_encoder_angle()
        if encoder_angle > turn - margin_of_error and encoder_angle < turn + margin_of_error:
            print("Observed value " + str(encoder_angle) + " tracks to " + str(turn) + ".")
        else:
            print("Encoder outside of tollerance! " + str(turn) + " vs " + str(encoder_angle))
        time.sleep(1)
        motor.reset()
            

if __name__ == "__main__":
    main()