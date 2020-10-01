import Adafruit_BBIO.GPIO as GPIO

# Tests just an encoder on pins P1-2 and P1-4, depends on the manual turning of the encoder
def main():
    # Pocket Beagle Encoder Channel A and B
    ch_a = "P1_2"
    ch_b = "P1_4"
     
    GPIO.setup(ch_a, GPIO.IN)
    GPIO.setup(ch_b, GPIO.IN)
    
    cha_st = GPIO.input(ch_a)
    chb_st = GPIO.input(ch_b)
    
    deg = 0
    i = 0
    while True:
        a_new = GPIO.input(ch_a)
        b_new = GPIO.input(ch_b)
        
        # If channel A is a rising edge
        if a_new == 1 and cha_st == 0:
            # If channel B is already high, clockwise turn 
            if chb_st == 1:
                deg += 0.703125
            # Else, CCW
            else:
                deg -= 0.703125
 
        # Update states
        cha_st = a_new
        chb_st = b_new
        
        # Time spent printing likely misses cycles, so do it infrequently
        if i % 600000 == 0:
            print(deg)
        i += 1
    

if __name__ == "__main__":
    main()