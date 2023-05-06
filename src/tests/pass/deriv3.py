import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

# sin(x)' = cos(x)
# cos(x)' = -sin(x)

result = wrapper.run_code("deriv(cos, 60 * pi / 180)")

if round(result, 3) == -0.866:
    exit(0)

exit(1)
