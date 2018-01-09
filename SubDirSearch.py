import os

class Search:
    def __init__(self):
        return

    def file_search(self, dir_path, ext_type):
        list_filepath = []
        for(path, dir, files) in os.walk(dir_path):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == ext_type:
                    print("%s" % path)
                    print("%s" % filename)
                    list_filepath.append(path+filename)
        return list_filepath
