from Triage import *
from BPlistParse import *

import subprocess

def main():
    print("Plist Forensics Analyzer")
    #root_dir = input("Input Root Directory to search plist files : ")
    #root_dir = "c:/Users/jschoi/Desktop/"
    evi_path = "G:\\Test_Macbook_500GB\\E01Capture.E01"
    Triage.get_plist_in_evi(Triage, evi_path)

    #for file in list_path:
    #    BPlistParse.read_bplist(BPlistParse, file)
    #    BPlistParse.SystemVersion(BPlistParse, file)

main()
