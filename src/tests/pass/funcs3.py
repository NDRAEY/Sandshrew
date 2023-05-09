import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("a(x) = { w = x + 8; w - 2 }; return a(1);")

if result == 7:
    exit(0)

exit(1)
