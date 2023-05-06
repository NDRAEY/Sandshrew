import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("a = 29; |-a|")

if round(result) == 29:
    exit(0)

exit(1)
