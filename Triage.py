# triage.py
# for getting plist file contents in Digital Evidence
# Date 2018.01.26
# Author by. Samuel Choi

import subprocess
import os

class Triage:
    def __init__(self):
        return

    def get_path_info(self, in_path, index_order):
        list_path = in_path.split()
        out_path = list_path[index_order]

        if index_order == 1:
            if out_path[-1] == ':':
                out_path[-1] = ''
                return out_path

        if index_order == 2:
            return out_path.split(".")[-1]

    def get_plist_in_evi(self, evi_path):

        filesystem_type = "hfs"
        image_type = "ewf"
        fls_cmd = "./sleuthkit-4.5.0-win32/bin/fls.exe -F -p -r -f %s -i %s %s" %(filesystem_type, image_type, evi_path)

        #fls_result = open("./fls_result.txt", 'w')

        #subprocess.call(fls_cmd, stdout=fls_result, timeout=None)
        #print(fls_cmd)

        #fls_result.close()

        get_fls_file = open("./fls_result.txt", 'r')
        triage_file = open("./triage_result.txt", 'w')

        while True:
            each_line = get_fls_file.readline()
            if not each_line:
                break
            ext = Triage.get_path_ext(Triage, each_line, 2)
            
            if ext == "plist":
                triage_file.write(each_line)

        get_fls_file.close()
        triage_file.close()