import serial
import Adafruit_BBIO.UART as UART

from Cube import Cube

from third_party_solver import solver

from tests import test_encoder_motor #, test_track_user_turns


def subsystem_build_test_demo():
	"""
	This phase demo focuses on three things:
	1.	Demonstrate functionality using the PocketBeagle (as opposed to the K64F from previous phases), included peripheral control and core solving algorithm.
	2.	Demonstrate Tablet <-> Bluetooth <-> PocketBeagle integration and control of the PocketBeagle via the tablet.
	3.	Demonstrate the ability to turn one or more stepper motors
	4.	Demonstrate the ability to accurately read the selected encoder

	Suggested future phase demos:
	1.	All six motors (only five here)
	2.	All six encoders (only one here)
	3.	Full range of Tablet functionality
	4.	Safety testing
	"""
	# UART2 Initialization
	UART.setup("PB-UART2")
	
	# A scrambled cube, 40 moves to mess up
	test_cube = Cube(enable_motors=True, debug=False, verbose=False)
	test_cube.scramble()
		
	# 1) Start comms with the connect Bluetooth device
	print("Starting comms and waiting for commands")
	with serial.Serial(port = "/dev/ttyO2", baudrate=9600) as ser:
		ser.write(b"Comms connected\r\n")
		while True:
			
			# TODO this is a hack, fix it when time allows, the app sends commands prefixed with a null
			# byte that throws off the string comparison, so it's stripped out here.
			line = ser.readline()
			line = line[1:] if int(line[0]) == 0 else line
			line = str(line.decode("utf-8").rstrip())
			
			# Built in commands are two capital letters, custom commands are lowercase words
			# pocker beagle responds with "PB" prefix and an echo of the command
			print("Got command: '" + line + "'")
			# Start a solve
			if line == "ST":
				# Acknowledge start with the number of moves the user took
				ser.write(str("PBST(" + str(test_cube.num_user_turns) + ")\r\n").encode("utf-8"))
				
				# Take the time to digest what the user moves were
				test_cube.prep_for_solve(ser)
				
				# Run the solving algo
				solve_cmds = solver.solve(str(test_cube), 25, 10)
				
				# Write the number of moves it will take
				ser.write(("PBMV(" + str(solve_cmds[solve_cmds.find("(") + 1 :solve_cmds.find(")") - 1]) + ") ").encode("utf-8"))
				
				# If there's moves to perform, do it.
				if solve_cmds.find("(") != 0:
					test_cube.digest_turns(solve_cmds[:solve_cmds.find("(")], ser)
				
				# Solution reached, stop the tablet's timer
				ser.write(b"PBSP\r\n")
				
				# Assert that this is correct
				if str(test_cube) != "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB":
					print(test_cube)
					assert False
			
			# Respond to a ping
			elif line == "PN":
				ser.write(b"PBPN\r\n")
			
			# Reset the Cube (zero motors and encoders)
			elif line == "RC":
				ser.write(b"PBRC")
				test_cube.reset()
			
			# Read some cube information
			elif line == "RD":
				ser.write(("PBRD:" + str(test_cube)).encode("utf-8"))
			
			# Verbose output
			elif line == "VB":
				ser.write(b"PBVB")
				test_cube.verbose = not test_cube.verbose
			
			# # Run the motor connected to the test encoder
			# elif line == "test":
			# 	ser.write(b"PBTS")
			# 	test_track_user_turns.main()
				
			# Run the encoder test
			elif line == "encoder":
				ser.write(b"PBEN")
				test_encoder_motor.main()
			
			# Simulate a user scramble
			elif line == "scramble":
				ser.write(b"PBSC")
				test_cube.scramble()
				
			# Terminate listening to BLE
			elif line == "exit":
				ser.write(b"PBXT")
				return
			

def main():
	subsystem_build_test_demo()

if __name__ == '__main__':
	main()