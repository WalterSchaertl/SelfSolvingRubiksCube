import Adafruit_BBIO.UART as UART
import serial

def main():
    # TODO add comand to app that auto accents "Test sending" and returns a 
    # success code, and failue on time out, and verify baud rate
    
    # Requires some setup to run, connect UART0-TX (P1-30) to bluetooth board TX, UART0-RX (P1-32) to blutooth baord RX, 
    UART.setup("PB-UART0")

    with serial.Serial(port = "/dev/ttyO0", baudrate=9600) as ser:
        print("Serial is open! Writing command")
        ser.write(b"Test sending\r\n")
        # Manually verify the command sent, send a response.
        print("Read a line from blutooth connection: " + str(ser.readline()))
    print("Bluetooth tests passed")

if __name__=="__main__":
    main()