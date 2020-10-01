# Self Solving Rubik's Cube
Senior Design Project to create a Self Solving Rubik's Cube, with the
core software running on a Pocket Beagle (https://beagleboard.org/pocket).
A Pocket Beagle interfaces with six motors, six encoders, and a Bluetooth
module. The motors each turn one of the six sides, the encoders act as
feedback to track the turns a user made to scramble the cube, and a
Bluetooth module to communicate with an app for a user interface.

## Setting up the Pocket Beagle

Set up the beagle board with the latest images and connect to wifi.
Steps can be found here: https://beagleboard.org/getting-started.

Wifi can be set up locally by running the wifi script, but must be also
configured on the host end, here is a good tutorial:
https://www.digikey.com/en/maker/blogs/how-to-connect-a-beaglebone-black-to-the-internet-using-usb


## Running The Project

1. Change directory to the place you want to run/develop:
```cd /var/lib/cloud9 ```
2. Clone this project:
```git clone https://github.com/WalterSchaertl/SelfSolvingRubiksCube.git```
3. Source environment variables (edit if needed for a different directory).
This needs to be done every time the board boots.
```source env_var.source```
4. Run the test scripts to ensure everything is working.
    1. If test_imports fails, ensure your python path is correct.
    2. If test_timing fails, try deleting the third_party_solver/tables
    folder and running again. The third party solver with then remake the
    tables. This may take more than 24 hours.
    3. If test_turning fails, try increasing the time limits and turn amounts,
    or relaxing the solving constraints. It's possible the solver is finding
    another, but equally valid, solution.
5. The next tests depend on the hardware being correctly wired.
    1. The test_bluetooth.py tests the the ability of the Pocket Beagle
    to connect to a Bluetooth device. On android, Serial Bluetooth
    Terminal is a working app.
    2. The test_motor.py tests the ability to turn all 6 motors.
    3. The test_encoder.py tests reading a single, hand manipulated encoder.
    4. The test_encoder_motor.py tests that the encoder roughly matches
    the expected position of a turning motor.

## Third Part Software

The core solving algorithm is a minimally changed version of the code found here:
https://github.com/hkociemba/RubiksCube-TwophaseSolver.

### Pip dependeincies

```pip3 install pyserial```

## Hardware

1. Main board: 1 Pocket Beagle Board: https://beagleboard.org/pocket
2. Encoders: 6 ENC-A4TS-0360-197-H-M: https://www.anaheimautomation.com/products/encoder/incremental-rotary-item.php?sID=351&serID=2&pt=i&tID=1054&cID=422
3. Motors/Drivers: 6 28BYJ-48 Stepper Motors, 6 ULN2003 Driver Boards: https://www.amazon.com/ELEGOO-28BYJ-48-ULN2003-Stepper-Arduino/dp/B01CP18J4A
4. Bluetooth: 1 HM-10 4.0 BLE module: http://www.dsdtech-global.com/2017/08/hm-10.html
5. Display: Samsung Galaxy Tab A: SM-P580
6. Various pin headers/cables/resistors required for construction
7. 3D printed cube chassis and pieces

## Display Software

The display software was made with MIT App Inventor, and an android .apk
is included in this repo.