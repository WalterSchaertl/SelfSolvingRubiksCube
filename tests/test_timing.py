from third_party_solver import solver
from Cube import Cube
from third_party_solver.enums import Color as Side
import time


def test_timing():
    cubestring = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"
    #solution = "D2 L3 D3 L2 U1 R2 F1 B1 L1 B1 D3 B2 R2 U3 R2 U3 F2 R2 U3 L2 (20f)"
    start = time.time()
    ret = solver.solve(cubestring, 25, 30)
    end = time.time()
    #assert ret == solution
    print(ret)
    assert (end - start) < 20
    print("Passed timing test with time to solve: " + str(end - start))
    
test_timing()
