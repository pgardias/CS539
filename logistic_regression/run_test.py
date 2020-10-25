from part1 import *
from test1 import *

if __name__ == "__main__":
	test_python_version()
	test_compute_z()
	test_compute_a()
	test_compute_L()
	test_forward()
	test_compute_dL_da()
	test_compute_da_dz()
	test_check_dz_dw()
	test_check_dz_db()
	test_backward()
	test_compute_dL_dw()
	test_compute_dL_db()
	test_update_w()
	test_update_b()
	test_train()
	test_predict()
	exit()
