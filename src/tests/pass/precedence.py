import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

result = wrapper.run_code("2 + 2 * 2")

if result == 6:
    exit(0)

print("2 + 2 * 2 = 6")
print("Но интерпретатор вернул:", result)
exit(1)
