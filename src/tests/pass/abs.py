import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("|-90|")

if round(result) == 90:
    exit(0)

exit(1)
