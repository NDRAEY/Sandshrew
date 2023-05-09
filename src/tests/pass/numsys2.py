import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("0x1234 + 0o7654 - 0b101001001")

if round(result) == 8343:
    exit(0)

exit(1)
