#!/usr/bin/env python3

"""this is main example"""

import os.path
import psutil

class ProcInfo:
    """processes with informat we can read"""
    processes = dict()
    file_r_idx = dict()
    file_path_r_idx = dict()
    def add_ps_name(self, pid, ps_name):
        """add process name"""
        self.processes[pid] = ps_name
    def addpath(self, path1, pid1):
        """addpath: to index"""
        base1 = os.path.basename(path1)
        if base1 in self.file_r_idx:
            self.file_r_idx[base1].add(path1)
        else:
            self.file_r_idx[base1] = {path1}

        if path1 in self.file_path_r_idx:
            self.file_path_r_idx[path1].add(pid1)
        else:
            self.file_path_r_idx[path1] = {pid1}

def main():
    """main function"""
    pinfo = ProcInfo()
    for pid in psutil.pids():
        ps1 = psutil.Process(pid)
        pinfo.add_ps_name(pid, ps1.name)
        try:
            ofs = ps1.open_files()
            ofmaps = ps1.memory_maps()

            for of1 in ofs:
                pinfo.addpath(of1.path, pid)
            for ofm in ofmaps:
                pinfo.addpath(ofm.path, pid)
        except (psutil.AccessDenied, psutil.NoSuchProcess, PermissionError):
            # print(process.name() + " Can't be read")
            pass
        else:
            pass
    print("======================")
    print(pinfo.file_r_idx)

# p.open_files()
# p.memory_maps
# psutil.AccessDenied

if __name__ == '__main__':
    main()
