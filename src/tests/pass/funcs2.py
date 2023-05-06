import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("a(x) = |(70 - x)| / 2!; return a(5)")

if result == 32.5:
    exit(0)

exit(1)
