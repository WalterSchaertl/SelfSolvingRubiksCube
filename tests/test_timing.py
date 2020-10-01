# Confirms the the cube can compute a solve (or fail) in a reasonable time to stop infinite loops
from third_party_solver import solver
import time


def test_timing():
	# Same solution is not always guaranteed, run test_turning for that
	cube_string = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"
	start = time.time()
	solver.solve(cube_string, 25, 30)
	end = time.time()
	assert (end - start) < 20
	print("Passed timing test with time to solve: " + str(end - start))


def main():
	test_timing()

if __name__ == "__main__":
	main()

