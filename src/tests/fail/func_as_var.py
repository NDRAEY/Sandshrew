import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

import wrapper

# Переменная не может быть функцией

a = wrapper.run_code("y = {}")
