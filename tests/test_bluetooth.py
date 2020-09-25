# Must be run with sudo
import Adafruit_BBIO.UART as UART
import serial

def main():
    # Requires some setup to run
    #  1. source env_var.source
    #  2. Connect P1_8 (UART2-RX) to HM-10 TX
    #  3. Connect P1_10 (UART2-TX) to HM-10 RX
    #  4. Connect power and ground
    UART.setup("PB-UART2")

    with serial.Serial(port = "/dev/ttyO2", baudrate=9600) as ser:
        print("Serial is open! Writing command")
        ser.write(b"Test sending\r\n")
        # Manually verify the command sent, send a response.
        print("Read a line from blutooth connection: " + str(ser.readline()))
    print("Bluetooth tests passed")

if __name__=="__main__":
    main()