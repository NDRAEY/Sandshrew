import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("D(a, b, c) = (b^2) - 4 * a * c; return D(1, 2, 3)")

if result == 2**2 - 4*1*3:
    exit(0)

exit(1)
