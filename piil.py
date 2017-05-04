#!/usr/bin/env python3

"""this is main example"""


import psutil

ar = psutil.pids()

print("Number of processes:")
print(len(ar))

print()
print("They are:")
print(ar)

