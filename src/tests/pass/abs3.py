import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("a = 3; -|-a|")

if round(result) == -3:
    exit(0)

exit(1)
