import numpy as np
from Motors import Motors
from third_party_solver import enums
from third_party_solver.enums import Color as C


class Cube:

	# A list of side faces where the index is the face side
	state = np.int8(
			[[[z for x in range(3)] for y in range(3)] for z in C] # * 10 + (x + y * 3)
	)
	
	def __init__(self, enable_motors: bool = False):
		# Enalbeing to motors slows the tests waaaaay down, so selectivly enable
		self.motors = Motors() if enable_motors else None
		self.enable_motors = enable_motors

	# # Single clockwise roatation
	# def turn_front_cw(self):
	# 	# Rotate the front
	# 	self.state[C.F] = np.rot90(self.state[C.F], k=3)
	#
	# 	# Shift the sides that boarder the front clockwise
	# 	temp = self.state[C.L][:,2].copy()  # save Left face right column
	# 	self.state[C.L][:, 2] = self.state[C.D][0, :]  # Left Face right column gets Down Face top row
	# 	self.state[C.D][0, :] = self.state[C.R][:, 0]  # Down Face top row gets Right Face left column
	# 	self.state[C.R][:, 0] = self.state[C.U][2, :]  # Right Face left column gets Up Face bottom row
	# 	self.state[C.U][2, :] = temp  				   # Up Face bottom row gets Left Face right column
	#
	# def turn_front_ccw(self):
	# 	self.state[C.F] = np.rot90(self.state[C.F], k=1)
	# 	temp = self.state[C.L][:, 2].copy()
	# 	self.state[C.L][:, 2] = self.state[C.U][2, :]  # Left Face right column gets Up Face Bottom Row
	# 	self.state[C.U][2, :] = self.state[C.R][:, 0]  # Up Face bottom row gets Right Face left column
	# 	self.state[C.R][:, 0] = self.state[C.D][0, :]  # Right Face left column gets Down Face top row
	# 	self.state[C.D][0, :] = temp                   # Down Face top row gets Left Face right column

	# Turn the face cw or ccw n times

	def turn_face_90(self, face: C, cw: bool):
		"""
		:param face: The face to turn
		:param cw: If turning clockwise (true) or counterclowise (false)
		:return: no return
		"""
		if self.enable_motors:
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
				s1, s2, s3, s4 = [C.B, C.D, C.F, C.U] # Up and Back
			else:
				s1, s2, s3, s4 = [C.B, C.U, C.F, C.D] # Back and Down
			temp = self.state[s1][:, rc1].copy()
			self.state[s1][:, rc1] = self.state[s2][:, rc2][::-1]
			self.state[s2][:, rc2] = self.state[s3][:, rc3]
			self.state[s3][:, rc3] = self.state[s4][:, rc4]
			self.state[s4][:, rc4] = temp[::-1]
		elif face == C.R:
			rc1, rc2, rc3, rc4 = 0, 2, 2, 2
			if cw:
				s1, s2, s3, s4 = [C.B, C.U, C.F, C.D] # Back and DOwn (1 and 4)
			else:
				s1, s2, s3, s4 = [C.B, C.D, C.F, C.U] # Up and Back
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
	def turn_face_180(self, face: C, cw: bool = True):
		self.turn_face_90(face, cw)
		self.turn_face_90(face, cw)

	def digest_turns(self, turns: str):
		# Expects a squence of two character space sperated. The first character is the turn face, and the
		# second is the number of times to turn, all turns are clockwise
		# TODO include physical turns
		cmds = turns.strip().split(" ")
		for cmd in cmds:
			face = C[cmd[0]]
			turn_num = int(cmd[1])
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

	def __str__(self):
		ret = ""
		for i in range(6):
			for col in self.state[i]:
				for square in col:
					ret += C(square).name
		return ret

	def pretty_print(self):
		ret = str(self)
		for i in range(3):
			print("    " + ret[i * 3 + 0] + ret[i * 3 + 1] + ret[i * 3 + 2])
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
			print("    " + ret[i * 3 + 0] + ret[i * 3 + 1] + ret[i * 3 + 2])
		print("")

"""""
	    The names of the facelet positions	 of the cube
	                  |************|
	                  |*U1**U2**U3*|
	                  |************|
	                  |*U4**U5**U6*|
	                  |************|
	                  |*U7**U8**U9*|
	                  |************|
	     |************|************|************|************|
	     |*L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*|
	     |************|************|************|************|
	     |*L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*|
	     |************|************|************|************|
	     |*L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*|
	     |************|************|************|************|
	                  |************|
	                  |*D1**D2**D3*|
	                  |************|
	                  |*D4**D5**D6*|
	                  |************|
	                  |*D7**D8**D9*|
	                  |************|
	    A cube definition string "UBL..." means for example: In position U1 we have the U-color, in position U2 we have the
	    B-color, in position U3 we have the L color etc. according to the order U1, U2, U3, U4, U5, U6, U7, U8, U9, R1, R2,
	    R3, R4, R5, R6, R7, R8, R9, F1, F2, F3, F4, F5, F6, F7, F8, F9, D1, D2, D3, D4, D5, D6, D7, D8, D9, L1, L2, L3, L4,
	    L5, L6, L7, L8, L9, B1, B2, B3, B4, B5, B6, B7, B8, B9 of the enum constants.
	    """
	# See nums for cube layout

