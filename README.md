# Self Solving Rubik's Cube
Senior Design Project to create a Self Solving Rubik's Cube, with the core
software running on a Pocket Beagle (https://beagleboard.org/pocket).


## Setting up the Pocket Beagle

Set up the beagle board and connect to wifi. Steps can be found here:
https://beagleboard.org/getting-started.

Wifi can be set up locally by running the wifi script, but must be also
configured on the host end, here is a good tutorial:
https://www.digikey.com/en/maker/blogs/how-to-connect-a-beaglebone-black-to-the-internet-using-usb


## Running The Project

1. Change directory to the place you want to run/develop:
```cd /var/lib/cloud9 ```
2. Clone this project:
```git clone https://github.com/WalterSchaertl/SelfSolvingRubiksCube.git```
3. Source environment variables (edit if needed for a different directory)
```source env_var.source```
4. Run the test scripts to ensure everything is working.
    1. If test_imports fails, ensure your python path is correct.
    2. If test_timing fails, try deleting the third_party_solver/tables
    folder and running again. The third party solver with then remake the
    tables. This may take more than 24 hours.
    3. If test_turning fails, try increasing the time limits and turn amounts,
    or relaxing the solving constraints. It's possible the solver is finding
    another, but equally valid, solution.

## Third Part Software

The core solving algorithm is a minimally changed version of the code found here:
https://github.com/hkociemba/RubiksCube-TwophaseSolver.

### Pip dependeincies

```pip3 install pyserial```

## Hardware

1. Pocket Beagle Board
2. TODO rest (encoders/motors/bluetooth ext.)

## Display Software

The display software was made with MIT App Inventor, and the .apk can be
found on the team's drive.