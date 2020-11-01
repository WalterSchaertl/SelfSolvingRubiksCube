# Test to see if
# 	1) The internal cube state tracker (Cube) can turn sides (test_single_turns)
# 	2) A cube with 40 random turns can be solved by the third_party_solver (test_solving)
# 	3) The response from the third_part_solver can be correctly digested to solve the cube (test_solving)

from third_party_solver import solver
from Cube import Cube
from third_party_solver.enums import Color as Side
import random
import time


def test_single_turns():
	# Map of side to expected [cw, ccw] turns
	test_cube = Cube()
	blank_cube = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
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
	assert str(test_cube) == blank_cube
	for side in expected.keys():
		test_cube.turn_face_90(side, True)
		assert str(test_cube) == expected[side][0]
		test_cube.turn_face_180(side, False)
		assert str(test_cube) == expected[side][1]
		test_cube.turn_face_90(side, True)
		assert str(test_cube) == blank_cube
	print("Passed single side turn test")


def test_solving():
	total_solve_time = 0.0
	num_trials = 10
	num_moves = 40
	# Solve 10 scrambles, each messed up with 40 random turns
	for x in range(num_trials):
		testCube = Cube()
		testCube.scramble(num_moves)
		# Assert that is could be solved in 25 moves in 10 seconds (more than enough)
		start = time.time()
		solve_cmds = solver.solve(str(testCube), 25, 10)
		total_solve_time += (time.time() - start)
		assert solve_cmds[-2:] == "f)"
		# Assert that the turn commands can be correctly digested to return the cube to a solved state
		# print(solve_cmds)
		testCube.digest_turns(solve_cmds[:solve_cmds.find("(")])
		assert str(testCube) == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
	print("Passed solving test, average time per solve " + str(total_solve_time / num_trials))


def main():
	test_single_turns()
	test_solving()

if __name__ == "__main__":
	main()
