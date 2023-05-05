import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("(8x)'")

if round(result) == 8:
    exit(0)

exit(1)
