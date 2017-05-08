#!/usr/bin/env python3

"""search over maps and fds on what file resource process is current using"""

import argparse
import os.path
import psutil

class ProcInfo:
    """processes with informat we can read"""
    file_r_idx = dict()
    file_path_r_idx = dict()
    def addpath(self, path1, pid1, ps_name):
        """addpath: to index"""
        base1 = os.path.basename(path1)
        if base1 in self.file_r_idx:
            self.file_r_idx[base1].add(path1)
        else:
            self.file_r_idx[base1] = {path1}

        pid_name = str(pid1) + ':' + ps_name
        # pid_name = ':' + ps_name
        if path1 in self.file_path_r_idx:
            self.file_path_r_idx[path1].add(pid_name)
        else:
            self.file_path_r_idx[path1] = {pid_name}

def main(cfg):
    """main function"""
    pinfo = ProcInfo()
    for pid in psutil.pids():
        try:
            ps1 = psutil.Process(pid)
            name = ps1.name()
            ofs = ps1.open_files()
            ofmaps = ps1.memory_maps()

            for of1 in ofs:
                pinfo.addpath(of1.path, pid, name)
            for ofm in ofmaps:
                pinfo.addpath(ofm.path, pid, name)
        except (psutil.AccessDenied, psutil.NoSuchProcess, PermissionError, FileNotFoundError):
            pass
    for filename in pinfo.file_r_idx:
        source = filename
        target = cfg.search_strings[0]
        if cfg.ignorecase:
            source = source.lower()
            target = target.lower()
        if target in source:
            for full_filepath in pinfo.file_r_idx[filename]:
                print(full_filepath, pinfo.file_path_r_idx[full_filepath])

def parse_args():
    """parse command line argumens, will read sys.argv"""
    usage = '%(prog)s [ACTION] [BUILD SYSTEM ARGS] [DIRECTORIES] [OPTIONS]'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-i', '--ignorecase', action='store_true',
                        default=False, dest='ignorecase',
                        help='Whether we match in a ignore case way')

    parser.add_argument('search_strings', metavar='string', nargs=1,
                        help='Sub string to be search')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    CFG = parse_args()
    main(CFG)
