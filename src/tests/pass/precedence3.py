import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("-8 + -(1 + 2)")

if result == -11:
    exit(0)

exit(1)
