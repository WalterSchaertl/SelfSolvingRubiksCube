import Adafruit_BBIO.GPIO as GPIO
import time


def main():
    ch_a = "P1_8"
    ch_b = "P1_6"
     
    GPIO.setup(ch_a, GPIO.IN)
    GPIO.setup(ch_b, GPIO.IN)
    
    cha_st = GPIO.input(ch_a)
    chb_st = GPIO.input(ch_b)
    
    deg = 0
    i = 0
    while True:
        a_new = GPIO.input(ch_a)
        b_new = GPIO.input(ch_b)
        
        if(a_new == 1 and cha_st == 0):
            if chb_st == 1:
                deg += 0.703125
            else:
                deg -= 0.703125
 
        cha_st = a_new
        chb_st = b_new
        if i % 600000 == 0:
            print(deg)
        i += 1
    

if __name__ == "__main__":
    main()