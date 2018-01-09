from SubDirSearch import *
from BPlistParse import *

def main():
    print("Plist Forensics Analyzer")
    #root_dir = input("Input Root Directory to search plist files : ")
    root_dir = "c:/Users/jschoi/Desktop/"

    list_path = Search.file_search(Search, root_dir, ".plist")

    for file in list_path:
        BPlistParse.read_bplist(BPlistParse, file)
        BPlistParse.SystemVersion(BPlistParse, file)

main()