import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper
import math

result = wrapper.run_code("5!")

if round(result) == math.factorial(5):
    exit(0)

exit(1)
