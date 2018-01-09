import plistlib

class BPlistParse:
    def __init__(self):
        return

    def read_bplist(self, bplist):
        with open(bplist, 'rb') as fp:
            plist = plistlib.load(fp)
        return plist

    def SystemVersion(self, SystemVersionPlist):
        plist = BPlistParse.read_bplist(BPlistParse, SystemVersionPlist)
        ProductBuildVersion = plist["ProductBuildVersion"]
        ProductCopyright = plist["ProductCopyright"]
        ProductName = plist["ProductName"]
        ProductUserVisibleVersion = plist["ProductUserVisibleVersion"]
        ProductVersion = plist["ProductVersion"]
        print(ProductBuildVersion, ProductCopyright)