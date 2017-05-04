#!/usr/bin/env python3

"""this is main example"""

import os.path
import psutil

# processes with informat we can read
processes = dict()
file_r_idx = dict()
file_path_r_idx = dict()

def addpath(path1, pid1):
    """addpath: to index"""
    base1 = os.path.basename(path1)
    if base1 in file_r_idx:
        file_r_idx[base1].add(path1)
    else:
        file_r_idx[base1] = {path1}

    if path1 in file_path_r_idx:
        file_path_r_idx[path1].add(pid1)
    else:
        file_path_r_idx[path1] = {pid1}

for pid in psutil.pids():
    p = psutil.Process(pid)
    processes[pid] = p.name()
    try:
        ofs = p.open_files()
        ofmaps = p.memory_maps()

        for of in ofs:
            addpath(of.path, pid)
        for ofm in ofmaps:
            addpath(ofm.path, pid)
    except (psutil.AccessDenied, psutil.NoSuchProcess, PermissionError):
        # print(process.name() + " Can't be read")
        pass
    else:
        pass

#print(processes)
print("======================")


print(file_r_idx)

# p.open_files()
# p.memory_maps
# psutil.AccessDenied
