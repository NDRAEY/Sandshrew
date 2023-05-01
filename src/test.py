import os
import subprocess as sp
from colorama import Fore, Style

PASS = "tests/pass/".replace("/", os.sep)
FAIL = "tests/fail/".replace("/", os.sep)

PASSED = list(os.walk(PASS))[0][-1]
FAILED = list(os.walk(FAIL))[0][-1]

os.chdir(PASS)

passed = 0

for i in PASSED:
    print("TEST:", i, "=> ", end='')
    
    exitcode = sp.call(["python", i])

    if not exitcode:
        print(Fore.GREEN, end='')
        passed += 1
    else:
        print(Fore.RED, end='')
    
    print("PASS" if not exitcode else "FAIL", Style.RESET_ALL)

os.chdir("../..")
os.chdir(FAIL)

for i in FAILED:
    print("TEST (Should fail):", i, "=> ", end='')
    
    exitcode = sp.call(["python", i])

    if exitcode:
        print(Fore.GREEN, end='')
        passed += 1
    else:
        print(Fore.RED, end='')
    
    print("PASS" if not exitcode else "FAIL")
    print(Style.RESET_ALL, end='')

os.chdir("../..")


all_tests = len(PASSED) + len(FAILED)

print()
print(f"Всего тестов: {all_tests}")
print(f"Успешных тестов: {passed}/{all_tests}")
print(f"Проваленных тестов: {all_tests - passed}/{all_tests}")

