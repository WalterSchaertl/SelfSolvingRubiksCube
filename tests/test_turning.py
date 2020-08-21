from third_party_solver import solver
from Cube import Cube
from third_party_solver.enums import Color as Side
import random


def test_single_turns():
	# Map of side to expected [cw, ccw] turns
	testCube = Cube()
	blankCube = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
	expected = {Side.U: ["UUUUUUUUUBBBRRRRRRRRRFFFFFFDDDDDDDDDFFFLLLLLLLLLBBBBBB",
						 "UUUUUUUUUFFFRRRRRRLLLFFFFFFDDDDDDDDDBBBLLLLLLRRRBBBBBB"],
				Side.R: ["UUFUUFUUFRRRRRRRRRFFDFFDFFDDDBDDBDDBLLLLLLLLLUBBUBBUBB",
						"UUBUUBUUBRRRRRRRRRFFUFFUFFUDDFDDFDDFLLLLLLLLLDBBDBBDBB"],
				Side.F: ["UUUUUULLLURRURRURRFFFFFFFFFRRRDDDDDDLLDLLDLLDBBBBBBBBB",
						"UUUUUURRRDRRDRRDRRFFFFFFFFFLLLDDDDDDLLULLULLUBBBBBBBBB"],
				Side.D: ["UUUUUUUUURRRRRRFFFFFFFFFLLLDDDDDDDDDLLLLLLBBBBBBBBBRRR",
						"UUUUUUUUURRRRRRBBBFFFFFFRRRDDDDDDDDDLLLLLLFFFBBBBBBLLL"],
				Side.L: ["BUUBUUBUURRRRRRRRRUFFUFFUFFFDDFDDFDDLLLLLLLLLBBDBBDBBD",
						"FUUFUUFUURRRRRRRRRDFFDFFDFFBDDBDDBDDLLLLLLLLLBBUBBUBBU"],
				Side.B: ["RRRUUUUUURRDRRDRRDFFFFFFFFFDDDDDDLLLULLULLULLBBBBBBBBB",
						"LLLUUUUUURRURRURRUFFFFFFFFFDDDDDDRRRDLLDLLDLLBBBBBBBBB"]
			}
	assert str(testCube) == blankCube
	for side in expected.keys():
		testCube.turn_face_90(side, True)
		assert str(testCube) == expected[side][0]
		testCube.turn_face_180(side, False)
		assert str(testCube) == expected[side][1]
		testCube.turn_face_90(side, True)
		assert str(testCube) == blankCube
	print("Passed single side turn test")


def test_solving():
	# Solve 10 scrambles, each messed up with 20 random turns
	for x in range(10):
		testCube = Cube()
		for i in range(20):
			side = random.choice([x for x in Side])
			dir = random.choice([True, False])
			amt = random.choice([90, 180])
			if amt == 90:
				testCube.turn_face_90(side, dir)
			else:
				testCube.turn_face_180(side, dir)
		# Assert that is could be solved in 25 moves in 10 seconds (more than enough)
		solve_cmds = solver.solve(str(testCube), 25, 10)
		assert solve_cmds[-2:] == "f)"
		# Assert that the turn commands can be correctly digested to return the cube to a solved state
		testCube.digest_turns(solve_cmds[:solve_cmds.find("(")])
		assert str(testCube) == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
	print("Passed solving test")


def main():
	test_single_turns()
	test_solving()

if __name__ == "__main__":
	main()
