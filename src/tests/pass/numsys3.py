import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("0x565656 / 8 + 0b10100")

if result == 707294.75:
    exit(0)

exit(1)
