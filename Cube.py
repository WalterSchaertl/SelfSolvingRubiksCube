import numpy as np
import random
from Motors import Motors
from third_party_solver.enums import Color as C
import time

class Cube:

	# A list of side faces where the index is the face side
	state = np.int8(
			[[[z for x in range(3)] for y in range(3)] for z in C]
	)
	
	def __init__(self, enable_motors: bool = False, debug: bool = False, verbose: bool = False):
		"""
		The main cube, contains ways to turn the faces and solve the cube

		:param enable_motors: If to enable motor turning, added to allow logical tests to
		:param debug: Set to true to enable printing
		run without turning the faces.
		"""
		self.motors = Motors(turn_callback=self.track_user_turns) if enable_motors else None
		self.enable_motors = enable_motors
		self.debug = debug
		self.user_turns = []
		self.verbose = verbose
		self.num_user_turns = 0
		self.solving = False

	def get_user_turns(self):
		return self.user_turns
	
	def write_ble(self, ser):
		if self.verbose and ser is not None:
			ser.write(("PBRD:" + str(self)).encode("utf-8"))
			time.sleep(3)
		
	def track_user_turns(self, side: str, cw: bool):
		# Only care about this data if we're in the "scramble" phase
		if self.solving:
			return
		
		self.user_turns.append((side, cw))
		self.num_user_turns += 1
		# This really shouldn't be used, waiting on BLE during an interrupt on a high speed encoder will
		# destroy any semblance of accuracy, use only for debugging or demos. This updates the known
		# state of the cube.
		if self.debug or self.verbose:
			self.turn_face_90(side, cw)
			del self.user_turns[0]
			if self.debug:
				print(str(self))
	
	def prep_for_solve(self, ser=None):
		# Convert the user moves into logical turns
		for side, cw in self.user_turns:
			self.turn_face_90(side, cw)
		self.solving = True # Enter the solving phase 
		self.write_ble(ser)
			
	
	def turn_face_90(self, face: C, cw: bool) -> None:
		"""
		Turns the selected face 90 degrees clockwise of counterclockwise, if solving and enable_motors are both
		true, then also turn the motors, else just memory manipulation.

		:param face: The face to turn
		:param cw: If turning clockwise (true) or counterclockwise (false)
		:return: no return
		"""
		if self.enable_motors and self.solving:
			self.motors.turn_motor(face, 90, cw)
		if cw:
			self.state[face] = np.rot90(self.state[face], k=3)
		else:
			self.state[face] = np.rot90(self.state[face], k=1)

		# Front and Back faces have col, row, col, row pattern
		if face == C.F or face == C.B:
			if face == C.F:
				if cw:
					s1, s2, s3, s4, rc1, rc2, rc3, rc4 = [C.L, C.D, C.R, C.U, 2, 0, 0, 2]
				else:
					s1, s2, s3, s4, rc1, rc2, rc3, rc4 = [C.L, C.U, C.R, C.D, 2, 2, 0, 0]
			else:
				if cw:
					s1, s2, s3, s4, rc1, rc2, rc3, rc4 = [C.L, C.U, C.R, C.D, 0, 0, 2, 2]
				else:
					s1, s2, s3, s4, rc1, rc2, rc3, rc4 = [C.L, C.D, C.R, C.U, 0, 2, 2, 0]

			revCrit = (cw and face == C.F) or (not cw and face == C.B)
			temp = self.state[s1][:, rc1].copy()
			self.state[s1][:, rc1] = self.state[s2][rc2, :][::1 if revCrit else -1]
			self.state[s2][rc2, :] = self.state[s3][:, rc3][::-1 if revCrit else 1]
			self.state[s3][:, rc3] = self.state[s4][rc4, :][::1 if revCrit else -1]
			self.state[s4][rc4, :] = temp[::-1 if revCrit else 1]
		# Left and Right faces operate only on cols
		elif face == C.L:
			rc1, rc2, rc3, rc4 = (2, 0, 0, 0)
			if cw:
				s1, s2, s3, s4 = [C.B, C.D, C.F, C.U]  # Up and Back
			else:
				s1, s2, s3, s4 = [C.B, C.U, C.F, C.D]  # Back and Down
			temp = self.state[s1][:, rc1].copy()
			self.state[s1][:, rc1] = self.state[s2][:, rc2][::-1]
			self.state[s2][:, rc2] = self.state[s3][:, rc3]
			self.state[s3][:, rc3] = self.state[s4][:, rc4]
			self.state[s4][:, rc4] = temp[::-1]
		elif face == C.R:
			rc1, rc2, rc3, rc4 = 0, 2, 2, 2
			if cw:
				s1, s2, s3, s4 = [C.B, C.U, C.F, C.D]  # Back and DOwn (1 and 4)
			else:
				s1, s2, s3, s4 = [C.B, C.D, C.F, C.U]  # Up and Back
			temp = self.state[s1][:, rc1].copy()
			self.state[s1][:, rc1] = self.state[s2][:, rc2][::-1]
			self.state[s2][:, rc2] = self.state[s3][:, rc3]
			self.state[s3][:, rc3] = self.state[s4][:, rc4]
			self.state[s4][:, rc4] = temp[::-1]
		# Up and Down faces operate only on rows
		elif face == C.U or face == C.D:
			if face == C.U:
				rc1, rc2, rc3, rc4 = 0, 0, 0, 0
			else:
				rc1, rc2, rc3, rc4 = 2, 2, 2, 2
			if (cw and face == C.U) or (not cw and face == C.D):
				s1, s2, s3, s4 = [C.L, C.F, C.R, C.B]
			else:
				s1, s2, s3, s4 = [C.L, C.B, C.R, C.F]
			temp = self.state[s1][rc1, :].copy()
			self.state[s1][rc1, :] = self.state[s2][rc2, :]
			self.state[s2][rc2, :] = self.state[s3][rc3, :]
			self.state[s3][rc3, :] = self.state[s4][rc4, :]
			self.state[s4][rc4, :] = temp

	# TODO optimize this
	def turn_face_180(self, face: C, cw: bool = True) -> None:
		"""
		Turns the selected face 180 degrees clockwise of counterclockwise, if solving and enable_motors are both
		true, then also turn the motors, else just memory manipulation.

		:param face: The face to turn
		:param cw: If turning clockwise (true) or counterclockwise (false)
		:return: no return
		"""
		self.turn_face_90(face, cw)
		self.turn_face_90(face, cw)

	def digest_turns(self, turns: str, ser= None) -> None:
		"""
		When given a string of turns, iterate through and perform those turns.

		:param turns: a sequence of two character space separated. The first character is the turn face, and the
		second is the number of times to turn, all turns are clockwise. ex) B3 U2 R1
		:param ser: BLE serial connection
		:return: None
		"""
		
		cmds = turns.strip().split(" ")
		if self.debug:
			print("Commands: " + str(cmds), flush=True)

		if len(cmds) == 0:
			return
		for cmd in cmds:
			face = C[cmd[0]]
			turn_num = int(cmd[1])
			if self.debug:
				print("CMD: " + str(face) + " " + str(turn_num))
			if turn_num == 1:
				self.turn_face_90(face, True)
			elif turn_num == 2:
				self.turn_face_180(face)
			elif turn_num == 3:
				self.turn_face_90(face, False)
			else:
				print("WARNING: turning more than 3 or less than 1 times!")
				for i in range(turn_num):
					self.turn_face_90(face, True)
			self.write_ble(ser)
		

	def __str__(self) -> str:
		"""
		Returns a compact 54 character sequence string of the cube.

		:return: String representation of the cube
		"""
		ret = ""
		for i in range(6):
			for col in self.state[i]:
				for square in col:
					ret += C(square).name
		return ret

	def pretty_print(self) -> None:
		"""
		Prints the cube in a format that it's easy to see it's 3D state,
		see bottom of this file.

		:return: None
		"""
		ret = str(self)
		for i in range(3):
			print("	" + ret[i * 3 + 0] + ret[i * 3 + 1] + ret[i * 3 + 2])
		print("   /---\\")
		ret = ret[9:]
		for i in range(3):
			print(ret[i * 3 + 27] + ret[i * 3 + 28] + ret[i * 3 + 29], end="|")
			print(ret[i * 3 + 9] + ret[i * 3 + 10] + ret[i * 3 + 11], end="|")
			print(ret[i * 3 + 0] + ret[i * 3 + 1] + ret[i * 3 + 2], end="|")
			print(ret[i * 3 + 36] + ret[i * 3 + 37] + ret[i * 3 + 38])
		print("   \\---/")
		ret = ret[18:]
		for i in range(3):
			print("	" + ret[i * 3 + 0] + ret[i * 3 + 1] + ret[i * 3 + 2])
		print("")
	
	def scramble(self, num_turns: int = 40) -> None:
		"""
		Simulates a user messing up the cube, random side in a random direction
		(clockwise or counterclockwise) a random amount (90 or 180)

		:param num_turns: The number of turns to perform
		:return: Nothing
		"""
		self.reset()
		for i in range(num_turns):
			side = random.choice([x for x in C])
			dir = random.choice([True, False])
			if random.choice([90, 180]) == 90:
				self.turn_face_90(side, dir)
			else:
				self.turn_face_180(side, dir)
				self.user_turns.append((side, dir))
			self.num_user_turns += 1
			self.user_turns.append((side, dir))
	
	def reset(self) -> None:
		"""
		Resets the cube to a 'solved' state.

		:return: Nothing
		"""
		self.state = np.int8([[[z for x in range(3)] for y in range(3)] for z in C])
		if self.enable_motors:
			for motor in self.motors.motors.values():
				motor.reset()
		self.user_turns = []
		self.num_user_turns = 0
		self.solving = False
							
# Similar to the pretty print format;
# 		The names of the facelet positions	 of the cube
# 					  |************|
# 					  |*U1**U2**U3*|
# 					  |************|
# 					  |*U4**U5**U6*|
# 					  |************|
# 					  |*U7**U8**U9*|
# 					  |************|
# 		 |************|************|************|************|
# 		 |*L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*|
# 		 |************|************|************|************|
# 		 |*L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*|
# 		 |************|************|************|************|
# 		 |*L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*|
# 		 |************|************|************|************|
# 					  |************|
# 					  |*D1**D2**D3*|
# 					  |************|
# 					  |*D4**D5**D6*|
# 					  |************|
# 					  |*D7**D8**D9*|
# 					  |************|
# Where U, D, B, F, R, L are Up, Down, Back, Front, Left, and Right colors/sides.

