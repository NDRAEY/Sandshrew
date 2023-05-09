import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("0x10 + 0b1010")

if round(result) == 26:
    exit(0)

exit(1)
